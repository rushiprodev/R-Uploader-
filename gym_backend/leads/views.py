# gym_backend/leads/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # For disabling CSRF protection on this webhook endpoint
from .models import Lead
import json
import logging

# Get an instance of a logger for this module
logger = logging.getLogger(__name__)
# For simple console output during development, you can configure basic logging.
# Add this near the top of your settings.py or manage.py for global basic config:
# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


@csrf_exempt # Crucial for allowing POST requests from external services like GoHighLevel
def create_lead(request):
    # Log entry for any request to this endpoint
    logger.debug(f"Request received at create_lead. Method: {request.method}")

    if request.method == "POST":
        # --- START DETAILED DEBUGGING OUTPUT for POST requests ---
        print("="*80)
        print(f"[{__name__}] NEW POST REQUEST RECEIVED AT create_lead") # Using __name__ for module context
        print(f"[{__name__}] Request Path: {request.path}")
        print(f"[{__name__}] --- REQUEST HEADERS ---")
        for header, value in request.headers.items():
            print(f"[{__name__}] {header}: {value}")

        raw_body_for_logging = "Raw body not available or decoding failed" # Default
        try:
            # Attempt to decode for logging. This helps see what was sent if parsing fails.
            raw_body_for_logging = request.body.decode('utf-8')
            print(f"[{__name__}] --- RAW REQUEST BODY (Decoded for logging) ---")
            print(raw_body_for_logging)
        except Exception as e_decode_log:
            print(f"[{__name__}] Could not decode request.body as utf-8 for logging: {e_decode_log}")
            print(f"[{__name__}] Raw request.body bytes for logging: {request.body[:500]}...") # Print first 500 bytes
        print("="*80)
        # --- END DETAILED DEBUGGING OUTPUT ---

        try:
            # 1. Check Content-Type header
            content_type = request.headers.get('Content-Type', '').lower()
            if 'application/json' not in content_type:
                error_message = f"Invalid Content-Type. Expected 'application/json', got '{request.headers.get('Content-Type', 'Not provided')}'"
                logger.warning(f"{error_message}. Raw body (logged): {raw_body_for_logging}")
                return JsonResponse({"error": error_message}, status=415) # 415 Unsupported Media Type

            # 2. Parse JSON data from the request body
            try:
                # Use the already decoded raw_body_for_logging if it was successful,
                # otherwise, decode request.body directly.
                # This ensures we try to parse what was actually sent if logging decode failed.
                data = json.loads(request.body.decode('utf-8'))
            except UnicodeDecodeError as ude:
                logger.error(f"UnicodeDecodeError parsing JSON: {ude}. Raw body bytes: {request.body[:500]}...")
                return JsonResponse({"error": "Invalid character encoding in request body. Expected UTF-8."}, status=400)
            except json.JSONDecodeError as e_json:
                logger.error(f"Invalid JSON format. Error: {e_json}. Raw body (logged): {raw_body_for_logging}")
                return JsonResponse({"error": f"Invalid JSON format. Details: {str(e_json)}"}, status=400)

            # 3. Extract data fields
            name = data.get("full_name")
            email = data.get("email")
            phone = data.get("phone")

            # 4. Validate required fields
            if not all([name, email, phone]): # More concise check
                missing = [field for field, value in [("name", name), ("email", email), ("phone", phone)] if not value]
                error_message = f"Missing required fields: {', '.join(missing)}."
                logger.warning(f"{error_message} Received data: {data}. Raw body (logged): {raw_body_for_logging}")
                return JsonResponse({"error": error_message, "received_data_keys": list(data.keys())}, status=400)

            # 5. Create and save the lead
            # Consider adding a try-except block here for potential IntegrityError
            # if, for example, email is unique and a duplicate is submitted.
            try:
                lead_obj = Lead.objects.create(name=name, email=email, phone=phone)
                logger.info(f"Lead created successfully. ID: {lead_obj.id}, Name: {name}, Email: {email}")
                return JsonResponse({"message": "Lead created successfully", "lead_id": lead_obj.id}, status=201) # 201 Created
            except Exception as db_error: # Catching generic database errors, be more specific if needed
                logger.error(f"Database error while creating lead: {db_error}. Data: {data}", exc_info=True)
                return JsonResponse({"error": f"Could not save lead due to a database issue. Details: {str(db_error)}"}, status=500)


        except Exception as e_outer:
            # Catch any other unexpected errors during the POST processing
            logger.error(f"Unexpected error in POST processing: {e_outer}. Raw body (logged): {raw_body_for_logging}", exc_info=True)
            return JsonResponse({"error": f"An unexpected server error occurred. Details: {str(e_outer)}"}, status=500)

    else:
        # Handle methods other than POST
        logger.warning(f"Method Not Allowed ({request.method}) for {request.path}")
        return JsonResponse({"error": f"Method {request.method} Not Allowed for this endpoint. Use POST."}, status=405)