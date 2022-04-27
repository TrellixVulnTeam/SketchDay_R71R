from django.test import TestCase
from .ml import emotional_analysis
# Create your tests here.
class MLTests(TestCase):
    def test_ea_algorithm(self):
        input_data = {
            "data" : "매우 기쁜날입니다",
        }
        test_gnadi = emotional_analysis.EmotionAnalysis()
        response = test_gnadi.predict(input_data)