import os
import unittest
from unittest.mock import patch

from laclaugpt import model_routing


class ModelRoutingConfigTests(unittest.TestCase):
    def test_stage_override_is_explicit_and_does_not_require_default_change(self) -> None:
        with patch.dict(os.environ, {"LACLAUGPT_MODEL_SYNTHESIS": "gemma4:26b"}):
            self.assertEqual(model_routing.pick_model("synthesis"), "gemma4:26b")

    def test_existing_default_routing_is_preserved_pending_benchmark(self) -> None:
        self.assertEqual(model_routing.STAGE_ROUTING["discourse"], "12b")
        self.assertEqual(model_routing.STAGE_ROUTING["temporal"], "12b")
        self.assertNotIn("synthesis", model_routing.STAGE_ROUTING)

    def test_embedding_model_is_embedding_specific(self) -> None:
        self.assertIn("embedding", model_routing.pick_embedding_model().casefold())


if __name__ == "__main__":
    unittest.main()
