from supabase import Client
from database import get_supabase_client

def fetch_data(url: str):
    supabase: Client = get_supabase_client()   

    try:
        print(f"Fetching data for URL: {url}")
        response = supabase.table("scrapperDB").select("*").eq("url", url).execute()

        if not response.data:
            print("No data found for the given URL.")
            return {"error": "No data found for the given URL."}

        print(f"Data fetched successfully: {response.data}")
        return {"data": response.data}
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": str(e)}
