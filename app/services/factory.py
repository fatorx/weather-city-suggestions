from app.services.sentence_creator import SentenceCreatorService
from app.vendors.factory import VendorFactory


class ServiceFactory:

    async def create_sentence_service(self) -> SentenceCreatorService:
        vendor_factory = VendorFactory()

        weather_vendor = vendor_factory.create_weather()
        gemini_vendor = vendor_factory.create_gemini_ll()

        return SentenceCreatorService(weather_vendor, gemini_vendor)
