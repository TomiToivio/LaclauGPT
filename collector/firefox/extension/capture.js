/**
 * LaclauGPT Collector — Firefox capture layer.
 *
 * LaclauGPT-native network capture based on the historical 2024
 * LaclauGPT TikTok Scraper: intercept relevant public platform API
 * responses, copy the response body to the local collector backend,
 * and leave the website's own response stream unchanged.
 *
 * The content script can also forward embedded page-state JSON that never
 * appears as a separate XHR. Both paths converge on the same local backend.
 *
 * Academic research use only.
 */

(() => {
  "use strict";

  // Public default for a local collector backend. Study-specific backend
  // addresses and ports belong in Firefox profile/private runtime settings.
  const DEFAULT_BACKEND_URL = "http://127.0.0.1:8765";
  let backendUrl = DEFAULT_BACKEND_URL;
  browser.storage.local.get({ backend_url: DEFAULT_BACKEND_URL })
    .then(item => {
      const stored = (item.backend_url || "").toString().trim();
      backendUrl = stored.startsWith("http") ? stored : DEFAULT_BACKEND_URL;
    })
    .catch(() => {});

  const MATCHERS = {
    tiktok: /api\.tiktokv\.com|\/api\/(?:post|challenge)\/item_list|\/api\/user\/playlist|\/api\/search\/(?:item_list|general\/full)|\/api\/preload\/item_list/,
    x: /(?:^|\.)x\.com\/i\/api\/graphql|(?:^|\.)twitter\.com\/i\/api\/graphql|\/i\/api\/graphql(?:\/|\?|$)/,
    instagram: /\/api\/v1\/|\/graphql\/query(?:[/?]|$)/,
  };

  function platformFor(url) {
    for (const [platform, matcher] of Object.entries(MATCHERS)) {
      if (matcher.test(url || "")) return platform;
    }
    return null;
  }

  async function tabUrlFor(tabId) {
    if (tabId < 0) return "";
    try {
      const tab = await browser.tabs.get(tabId);
      return tab?.url || "";
    } catch {
      return "";
    }
  }

  async function postCapture({ platform, apiUrl, platformUrl, body }) {
    if (!platform || body === null || body === undefined || body === "") return false;
    try {
      const response = await fetch(`${backendUrl}/capture`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          platform,
          api_url: apiUrl || platformUrl || "",
          platform_url: platformUrl || apiUrl || "",
          captured_at: new Date().toISOString(),
          body,
        }),
      });
      if (!response.ok) {
        console.warn("[laclaugpt-collector] backend rejected capture", platform, response.status);
        return false;
      }
      return true;
    } catch (error) {
      console.warn("[laclaugpt-collector] backend unavailable", error);
      return false;
    }
  }

  async function sendCapture(details, platform, body, capturedPlatformUrl = "") {
    const platformUrl = capturedPlatformUrl || details.documentUrl || details.originUrl || "";
    return postCapture({ platform, apiUrl: details.url, platformUrl, body });
  }

  function captureResponse(details) {
    const platform = platformFor(details.url);
    if (!platform || ["HEAD", "OPTIONS"].includes(details.method)) return;

    const platformUrlPromise = tabUrlFor(details.tabId);

    let filter;
    try {
      filter = browser.webRequest.filterResponseData(details.requestId);
    } catch (error) {
      console.warn("[laclaugpt-collector] cannot attach response filter", error);
      return;
    }

    const decoder = new TextDecoder("utf-8");
    const chunks = [];

    filter.ondata = event => {
      chunks.push(decoder.decode(event.data, { stream: true }));
      filter.write(event.data);
    };

    filter.onerror = event => {
      console.warn("[laclaugpt-collector] response filter error", platform, event.error);
      try { filter.disconnect(); } catch {}
    };

    filter.onstop = async () => {
      chunks.push(decoder.decode());
      try { filter.close(); } catch {}
      const platformUrl = await platformUrlPromise;
      await sendCapture(details, platform, chunks.join(""), platformUrl);
    };
  }

  browser.webRequest.onHeadersReceived.addListener(
    captureResponse,
    { urls: ["<all_urls>"], types: ["xmlhttprequest"] },
    ["blocking"],
  );

  browser.runtime.onMessage.addListener(async (message, sender) => {
    if (message?.type !== "embedded") return undefined;
    if (!(["tiktok", "instagram"].includes(message.platform))) return { accepted: 0 };

    const payloads = Array.isArray(message.payloads) ? message.payloads : [];
    const pageUrl = sender?.tab?.url || message.page_url || "";
    let accepted = 0;

    for (const payload of payloads) {
      if (!payload || payload.body === undefined || payload.body === null) continue;
      const ok = await postCapture({
        platform: message.platform,
        apiUrl: `${pageUrl}#embedded:${payload.kind || "json"}`,
        platformUrl: pageUrl,
        body: payload.body,
      });
      if (ok) accepted += 1;
    }
    return { accepted };
  });

  setInterval(() => {
    fetch(`${backendUrl}/ping`, { method: "POST" }).catch(() => {});
  }, 60000);
})();
