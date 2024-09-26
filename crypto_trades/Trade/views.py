from django.shortcuts import render

# Create your views here.
import csv
from io import StringIO
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Trade


@api_view(["POST"])
def upload_csv(request):
    if "file" not in request.FILES:
        return Response(
            {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Read the uploaded CSV file
        file = request.FILES["file"]
        decoded_file = file.read().decode("utf-8")
        io_string = StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        # Prepare a list to bulk create Trade objects
        trades = []
        for row in reader:
            base_coin, quote_coin = row["Market"].split("/")
            operation = row["Operation"].lower()  # Normalize operation
            amount = float(row["Buy/Sell Amount"])
            price = float(row["Price"])

            trade = Trade(
                utc_time=row["UTC_Time"],
                operation=operation,
                base_coin=base_coin,
                quote_coin=quote_coin,
                amount=amount,
                price=price,
            )
            trades.append(trade)

        # Bulk create trades in the database
        Trade.objects.bulk_create(trades)
        return Response(
            {"message": "CSV uploaded and data saved successfully!"},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
