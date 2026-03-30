from models.customer import Customer
from models.service_provider import ServiceProvider
from models.booking import Booking
from models.review import Review


def load_sample_data():
    """
    Creates sample providers, customers, bookings, and reviews.
    Used to populate the app with test data.
    """


    provider1 = ServiceProvider(
        1, "Kamal Silva", "kamal@email.com", "pass123", "0771234567"
    )
    provider1.create_profile(
        "plumbing", 10, 1500, "Colombo",
        "Expert plumber with 10 years experience. Specializing in all plumbing repairs."
    )

    provider2 = ServiceProvider(
        2, "Nimal Perera", "nimal@email.com", "pass123", "0777654321"
    )
    provider2.create_profile(
        "plumbing", 5, 1000, "Kandy",
        "Affordable and reliable plumbing services for homes and offices."
    )

    provider3 = ServiceProvider(
        3, "Saman Fernando", "saman@email.com", "pass123", "0779876543"
    )
    provider3.create_profile(
        "carpentry", 8, 2000, "Colombo",
        "Custom furniture, door repairs, cabinets, and all wood work."
    )

    provider4 = ServiceProvider(
        4, "Ruwan Dias", "ruwan@email.com", "pass123", "0771112233"
    )
    provider4.create_profile(
        "electrical", 12, 1800, "Galle",
        "Licensed electrician for all residential and commercial electrical work."
    )

    provider5 = ServiceProvider(
        5, "Ajith Kumara", "ajith@email.com", "pass123", "0774445566"
    )
    provider5.create_profile(
        "painting", 6, 1200, "Colombo",
        "Interior and exterior painting specialist. Quality finish guaranteed."
    )

    provider6 = ServiceProvider(
        6, "Chaminda Bandara", "chaminda@email.com", "pass123", "0776667788"
    )
    provider6.create_profile(
        "cleaning", 3, 800, "Kandy",
        "Home and office deep cleaning services. Spotless results."
    )

    provider7 = ServiceProvider(
        7, "Lasith Malinga", "lasith@email.com", "pass123", "0778889900"
    )
    provider7.create_profile(
        "electrical", 7, 1500, "Colombo",
        "Wiring, switch repairs, fan installation, and circuit fixes."
    )

    provider8 = ServiceProvider(
        8, "Dinesh Priyantha", "dinesh@email.com", "pass123", "0770001122"
    )
    provider8.create_profile(
        "carpentry", 15, 2500, "Galle",
        "Master carpenter with 15 years experience. Premium furniture work."
    )

    all_providers = [
        provider1, provider2, provider3, provider4,
        provider5, provider6, provider7, provider8
    ]


    customer1 = Customer(
        101, "Ashan Bandara", "ashan@email.com",
        "pass123", "0712345678", "Colombo 05"
    )
    customer2 = Customer(
        102, "Dilini Jayawardena", "dilini@email.com",
        "pass123", "0723456789", "Kandy"
    )
    customer3 = Customer(
        103, "Nuwan Perera", "nuwan@email.com",
        "pass123", "0734567890", "Galle"
    )

    all_customers = [customer1, customer2, customer3]


    # Reviews for Kamal (Plumber)
    reviews_kamal = [
        Review(1, 101, "Ashan Bandara", 1, "Kamal Silva", 5,
               "Excellent work! Very professional and punctual. Fixed the leak quickly and cleanly.",
               "plumbing"),
        Review(2, 102, "Dilini Jayawardena", 1, "Kamal Silva", 4,
               "Good plumber, friendly and reliable. Quality work done on time. Reasonable price.",
               "plumbing"),
        Review(3, 103, "Nuwan Perera", 1, "Kamal Silva", 5,
               "Best plumber ever! Highly recommend. Expert service and very affordable.",
               "plumbing"),
        Review(4, 104, "Sachini Fernando", 1, "Kamal Silva", 4,
               "Professional service. Clean work area. Fast and efficient. Will hire again.",
               "plumbing"),
    ]
    for r in reviews_kamal:
        provider1.receive_review(r)

    # Reviews for Nimal (Plumber)
    reviews_nimal = [
        Review(5, 101, "Ashan Bandara", 2, "Nimal Perera", 3,
               "Average work. Was late and took too long. But price was reasonable.",
               "plumbing"),
        Review(6, 102, "Dilini Jayawardena", 2, "Nimal Perera", 2,
               "Poor service. Unprofessional and slow. Had to call again to fix the same issue.",
               "plumbing"),
        Review(7, 105, "Kasun Silva", 2, "Nimal Perera", 3,
               "OK work but not very skilled. Affordable though. Average experience.",
               "plumbing"),
    ]
    for r in reviews_nimal:
        provider2.receive_review(r)

    # Reviews for Saman (Carpenter)
    reviews_saman = [
        Review(8, 101, "Ashan Bandara", 3, "Saman Fernando", 5,
               "Amazing carpenter! Beautiful furniture. Very professional and skilled craftsman.",
               "carpentry"),
        Review(9, 102, "Dilini Jayawardena", 3, "Saman Fernando", 5,
               "Outstanding quality work. Expert craftsmanship. Highly recommend for any wood work!",
               "carpentry"),
        Review(10, 106, "Tharushi Perera", 3, "Saman Fernando", 4,
               "Great work on my kitchen cabinet. Neat and clean finish. Punctual and friendly.",
               "carpentry"),
    ]
    for r in reviews_saman:
        provider3.receive_review(r)

    # Reviews for Ruwan (Electrician)
    reviews_ruwan = [
        Review(11, 101, "Ashan Bandara", 4, "Ruwan Dias", 4,
               "Good electrician. Fixed the wiring issue quickly. Professional and experienced.",
               "electrical"),
        Review(12, 107, "Malik Jayasuriya", 4, "Ruwan Dias", 5,
               "Excellent! Expert electrician. Fast and reliable service. Highly skilled.",
               "electrical"),
        Review(13, 103, "Nuwan Perera", 4, "Ruwan Dias", 4,
               "Reliable and trustworthy. Good quality electrical work. Recommended.",
               "electrical"),
    ]
    for r in reviews_ruwan:
        provider4.receive_review(r)

    # Reviews for Ajith (Painter)
    reviews_ajith = [
        Review(14, 102, "Dilini Jayawardena", 5, "Ajith Kumara", 4,
               "Good painting work. Clean finish and friendly person. Quality paint used.",
               "painting"),
        Review(15, 108, "Roshani Silva", 5, "Ajith Kumara", 3,
               "Average painting. Color was good but took longer than expected. Slow work.",
               "painting"),
    ]
    for r in reviews_ajith:
        provider5.receive_review(r)

    # Reviews for Chaminda (Cleaning)
    reviews_chaminda = [
        Review(16, 101, "Ashan Bandara", 6, "Chaminda Bandara", 5,
               "Spotless cleaning! Very thorough and professional. Highly recommend this service.",
               "cleaning"),
        Review(17, 102, "Dilini Jayawardena", 6, "Chaminda Bandara", 4,
               "Good cleaning service. Everything was clean and neat. Punctual and careful.",
               "cleaning"),
    ]
    for r in reviews_chaminda:
        provider6.receive_review(r)

    # Reviews for Lasith (Electrician)
    reviews_lasith = [
        Review(18, 109, "Harsha Kumara", 7, "Lasith Malinga", 3,
               "Average work. Not very experienced with complex issues. Some delay in arrival.",
               "electrical"),
        Review(19, 110, "Sanduni Perera", 7, "Lasith Malinga", 2,
               "Poor quality work. Unprofessional behavior. The switch broke again after a week.",
               "electrical"),
    ]
    for r in reviews_lasith:
        provider7.receive_review(r)

    # Reviews for Dinesh (Carpenter)
    reviews_dinesh = [
        Review(20, 101, "Ashan Bandara", 8, "Dinesh Priyantha", 4,
               "Good carpenter. Very experienced and skilled. Quality work but bit expensive.",
               "carpentry"),
        Review(21, 111, "Kavinda Rathnayake", 8, "Dinesh Priyantha", 4,
               "Quality wood work. Professional finish. Recommended for premium furniture needs.",
               "carpentry"),
    ]
    for r in reviews_dinesh:
        provider8.receive_review(r)


    # Completed booking for Ashan with Kamal
    booking1 = Booking(
        customer_id=101, customer_name="Ashan Bandara",
        provider_id=1, provider_name="Kamal Silva",
        service_type="plumbing", booking_date="2025-01-15",
        description="Kitchen tap is leaking badly"
    )
    booking1.set_status("completed")
    customer1.book_service(booking1)
    provider1.receive_booking(booking1)

    # Pending booking for Dilini with Saman
    booking2 = Booking(
        customer_id=102, customer_name="Dilini Jayawardena",
        provider_id=3, provider_name="Saman Fernando",
        service_type="carpentry", booking_date="2025-02-10",
        description="Need new kitchen cabinet"
    )
    customer2.book_service(booking2)
    provider3.receive_booking(booking2)

    # Accepted booking for Nuwan with Ruwan
    booking3 = Booking(
        customer_id=103, customer_name="Nuwan Perera",
        provider_id=4, provider_name="Ruwan Dias",
        service_type="electrical", booking_date="2025-02-05",
        description="Ceiling fan not working"
    )
    booking3.set_status("accepted")
    customer3.book_service(booking3)
    provider4.receive_booking(booking3)

    return {
        "providers": all_providers,
        "customers": all_customers
    }