from django.shortcuts import render, redirect
from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from .models import Listing


def listing_list(request):
    sort_by = request.GET.get("sort", "newest")  # default sort by newest
    listings = Listing.objects.all()

    if sort_by == "price_asc":
        listings = listings.order_by("price_per_night")
    elif sort_by == "price_desc":
        listings = listings.order_by("-price_per_night")
    elif sort_by == "oldest":
        listings = listings.order_by("created_at")
    else:  # newest
        listings = listings.order_by("-created_at")

    return render(
        request,
        "listing_list.html",
        {
            "listings": listings,
            "sort_by": sort_by,
        },
    )


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)  # don't save to DB yet
            listing.owner = request.user  # set the owner to the logged-in user
            listing.save()  # now save to DB
            return redirect("listing_list")  # redirect after success
    else:
        form = ListingForm()
    return render(request, "create_listing.html", {"form": form})
