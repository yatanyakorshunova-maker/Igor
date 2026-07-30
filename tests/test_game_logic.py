import unittest

from game_logic import PetModel, clamp


class PetModelTests(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(-5), 0)
        self.assertEqual(clamp(55), 55)
        self.assertEqual(clamp(140), 100)

    def test_feed_changes_expected_values(self):
        pet = PetModel()
        message = pet.feed()
        self.assertEqual(pet.satiety, 70)
        self.assertEqual(pet.mood, 55)
        self.assertEqual(pet.energy, 50)
        self.assertEqual(pet.actions, 1)
        self.assertIn("вкусно", message.lower())

    def test_play_changes_expected_values(self):
        pet = PetModel()
        pet.play()
        self.assertEqual(pet.satiety, 45)
        self.assertEqual(pet.mood, 70)
        self.assertEqual(pet.energy, 35)

    def test_sleep_is_two_stage_action(self):
        pet = PetModel()
        pet.start_sleep()
        self.assertTrue(pet.sleeping)
        self.assertEqual(pet.image_state(), "sleep")
        pet.finish_sleep()
        self.assertFalse(pet.sleeping)
        self.assertEqual(pet.energy, 80)
        self.assertEqual(pet.satiety, 40)

    def test_image_state_priority(self):
        pet = PetModel(satiety=10, energy=10, mood=10)
        self.assertEqual(pet.image_state(), "hungry")
        pet.satiety = 50
        self.assertEqual(pet.image_state(), "tired")
        pet.energy = 50
        self.assertEqual(pet.image_state(), "sad")
        pet.mood = 90
        self.assertEqual(pet.image_state(), "happy")

    def test_reward_is_granted_once(self):
        pet = PetModel(satiety=80, mood=80, energy=80)
        self.assertTrue(pet.check_reward())
        self.assertEqual(pet.coins, 100)
        self.assertFalse(pet.check_reward())
        self.assertEqual(pet.coins, 100)

    def test_serialization_ignores_unknown_fields(self):
        pet = PetModel.from_dict({"name": "Луна", "satiety": 150, "unknown": "value", "sleeping": True})
        self.assertEqual(pet.name, "Луна")
        self.assertEqual(pet.satiety, 100)
        self.assertFalse(pet.sleeping)


if __name__ == "__main__":
    unittest.main()
