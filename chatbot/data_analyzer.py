"""
DATA RETRIEVER - The 'R' in RAG
Retrieves data from SQLite database and formats as text for Gemini.
"""

class DataRetriever:
    def __init__(self, db_manager):
        self.__db = db_manager

    def get_all_providers_context(self):
        """Get all providers as text"""
        providers = self.__db.get_all_providers()
        if not providers:
            return "No service providers are currently registered."

        context = "=== ALL SERVICE PROVIDERS ===\n\n"
        for provider in providers:
            context += self.__format_provider_text(provider)
            # Add reviews
            reviews = self.__db.get_provider_reviews(provider["id"])
            if reviews:
                context += f"  Customer Reviews ({len(reviews)} total):\n"
                for review in reviews:
                    context += (
                        f"    - Rating: {review['rating']}/5 | "
                        f"Customer: {review['customer_name']} | "
                        f"Review: \"{review['review_text']}\"\n"
                    )
            else:
                context += "  Customer Reviews: No reviews yet.\n"
            context += "\n" + "-" * 50 + "\n\n"
        return context

    def get_providers_by_service_context(self, service_type):
        """Get providers filtered by service type"""
        providers = self.__db.get_all_providers(service_type)
        if not providers:
            return f"No providers found for '{service_type}'."

        context = f"=== {service_type.upper()} PROVIDERS ===\n\n"
        for provider in providers:
            context += self.__format_provider_text(provider)
            reviews = self.__db.get_provider_reviews(provider["id"])
            if reviews:
                context += f"  Reviews ({len(reviews)}):\n"
                for review in reviews:
                    context += (
                        f"    - {review['rating']}/5: "
                        f"\"{review['review_text']}\"\n"
                    )
            context += "\n" + "-" * 50 + "\n\n"
        return context

    def build_context_for_query(self, user_message):
        """Auto-detect what data to retrieve based on user's question"""
        message = user_message.lower()
        services = ["plumbing", "carpentry", "electrical", "painting", "cleaning"]

        # Check if asking about a specific service
        for service in services:
            if service in message:
                return self.get_providers_by_service_context(service)

        # Default: return all providers
        return self.get_all_providers_context()

    def __format_provider_text(self, provider):
        """Format one provider's data as text"""
        text = f"  Provider: {provider['name']}\n"
        text += f"  Service: {provider['service_type']}\n"
        text += f"  Experience: {provider['experience']} years\n"
        text += f"  Hourly Rate: Rs.{provider['hourly_rate']}\n"
        text += f"  Location: {provider['location']}\n"
        text += f"  Description: {provider['description']}\n"
        text += f"  Average Rating: {provider['average_rating']}/5\n"
        text += f"  Total Reviews: {provider['review_count']}\n"
        return text