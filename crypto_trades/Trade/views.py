import csv
import io
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Trade
from django.utils import timezone


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith(".csv"):
                return render(
                    request,
                    "upload_csv.html",
                    {
                        "form": form,
                        "error_message": "The uploaded file is not a CSV file.",
                    },
                )

            decoded_file = csv_file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=",")
            next(reader)  # Skip the header row

            for row in reader:
                utc_time = row[0]
                operation = row[1]
                market = row[2]
                buy_sell_amount = row[3]
                price = row[4]

                base_coin, quote_coin = market.split("/")

                Trade.objects.create(
                    utc_time=timezone.datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S"),
                    operation=operation.upper(),
                    base_coin=base_coin,
                    quote_coin=quote_coin,
                    amount=buy_sell_amount,  # Assuming your field name is 'amount'
                    price=price,
                )

            # Retrieve all Trade data to display
            trades = Trade.objects.all()
            return render(
                request,
                "upload_success.html",
                {
                    "success_message": "File uploaded and data saved successfully!",
                    "trades": trades,
                },
            )
        else:
            return render(request, "upload_csv.html", {"form": form})
    else:
        form = CSVUploadForm()
    return render(request, "upload_csv.html", {"form": form})
