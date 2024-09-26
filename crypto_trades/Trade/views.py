import csv
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Trade
from django.utils import timezone
import io


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=",")
            next(reader)  # Skip the header row

            for row in reader:
                utc_time = row[0]  # Assuming this is in the first column
                operation = row[1]  # Assuming this is in the second column
                market = row[2]  # Assuming this is in the third column
                buy_sell_amount = row[3]  # Fourth column
                price = row[4]  # Fifth column

                # Split market to get base and quote coins
                base_coin, quote_coin = market.split("/")

                # Create and save Trade object
                Trade.objects.create(
                    utc_time=timezone.datetime.strptime(
                        utc_time, "%Y-%m-%d %H:%M:%S"
                    ),  # Adjust format as needed
                    operation=operation.upper(),
                    base_coin=base_coin,
                    quote_coin=quote_coin,
                    buy_sell_amount=buy_sell_amount,
                    price=price,
                )

            return render(
                request, "upload_success.html"
            )  # Redirect or render success page
    else:
        form = CSVUploadForm()
    return render(request, "upload_csv.html", {"form": form})
