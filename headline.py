
import requests
from bs4 import BeautifulSoup


URL = "https://www.bbc.com/news"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def get_top_headlines():
    try:
        # Step 1: Fetch the webpage
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=15
        )

        # Step 2: Check HTTP response status
        response.raise_for_status()

        # Step 3: Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 4: Extract headline elements
        headline_elements = soup.select(
            'h2[data-testid="card-headline"]'
        )

        # Step 5: Remove duplicates and empty headlines
        headlines = []
        seen = set()

        for element in headline_elements:
            headline = element.get_text(" ", strip=True)

            if not headline or headline in seen:
                continue

            seen.add(headline)
            headlines.append(headline)

            if len(headlines) == 5:
                break

        # Step 6: Display headlines
        print("\n===== TOP 5 BBC NEWS HEADLINES =====\n")

        if not headlines:
            print("No headlines found. The website structure may have changed.")
            return

        for index, headline in enumerate(headlines, start=1):
            print(f"{index}. {headline}")

        if len(headlines) < 5:
            print(f"\nOnly {len(headlines)} headlines were found.")

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the website.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")


if __name__ == "__main__":
    get_top_headlines()

