import csv
import logging
import os
from datetime import datetime

from google_play_scraper import Sort, reviews

logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_reviews_for_all_banks():
    apps = {
        "CBE": ("com.cbe.customerapp", "Commercial Bank of Ethiopia"),
        "BOA": ("com.bankofabyssinia.boamobile", "Bank of Abyssinia"),
        "Dashen": ("com.dashen.dashensuperapp", "Dashen Bank")
    }

    all_reviews = []

    for code, (app_id, bank_name) in apps.items():
        logging.info(f"🔄 Fetching reviews for {bank_name}")
        try:
            results, _ = reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=1500,  
                filter_score_with=None
            )

            for entry in results:
                all_reviews.append({
                    'review_text': entry['content'],
                    'rating': entry['score'],
                    'date': entry['at'].strftime('%Y-%m-%d'),
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })

            logging.info(f"✅ Collected {len(results)} reviews for {bank_name}")

        except Exception as e:
            logging.error(f"❌ Error scraping {bank_name}: {e}")

    # Save to combined CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'all_bank_reviews_{timestamp}.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['review_text', 'rating', 'date', 'bank_name', 'source'])
        writer.writeheader()
        writer.writerows(all_reviews)

    logging.info(f"✅ Saved all reviews to {filename}")
    print(f"Scraping completed. Reviews saved to {filename}")

if __name__ == "__main__":
    scrape_reviews_for_all_banks()
