from scraper import SongScraper


serial_name = input('Serial to extract songs from: ')
scraper = SongScraper(serial_name)
scraper.get_videos()
