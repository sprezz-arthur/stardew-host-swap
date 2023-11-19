from django.shortcuts import render, HttpResponse
from stardjango.utils import (
    get_host_data,
    get_players_data,
    get_name,
    add_mails,
    get_home_data,
    add_events,
)

OLD_HOST_DATA_PLACEHOLDER = "</ OLD_HOST_DATA>"
NEW_HOST_DATA_PLACEHOLDER = "</ NEW_HOST_DATA>"


def editor(request):
    context = {}

    if request.method != "POST":
        return render(request, "editor.html", context)

    file = request.FILES.get("file")
    if file is None:
        return render(request, "editor.html", context)

    file_content = file.read().decode("utf-8")

    context["file_content"] = file_content
    context["file_name"] = file.name

    players_data = get_players_data(file_content)
    host_data = get_host_data(file_content)

    assert players_data
    assert host_data

    farmers = [get_name(player) for player in [host_data, *players_data]]

    context["farmers"] = farmers
    context["selected_farmer_id"] = 0

    return render(request, "editor.html", context)


def download_file(request):
    if request.method == "POST":
        old_file_content = request.POST.get("file_content", "")
        file_name = request.POST.get("file_name")
        selected_farmer_id = int(request.POST.get("selected_farmer_id"))

        new_file_content = old_file_content

        old_host_data = get_host_data(old_file_content)
        new_host_data = get_players_data(old_file_content)[selected_farmer_id - 1]

        new_file_content = new_file_content.replace(
            old_host_data, OLD_HOST_DATA_PLACEHOLDER
        )
        new_file_content = new_file_content.replace(
            new_host_data, NEW_HOST_DATA_PLACEHOLDER
        )

        old_home_data = get_home_data(old_host_data)
        new_home_data = get_home_data(new_host_data)

        old_host_data, new_host_data = (
            old_host_data.replace(old_home_data, new_home_data),
            new_host_data.replace(new_home_data, old_home_data),
        )

        # Otherwise Community Center (and possibliy other things) can get locked
        new_host_data = add_mails(
            giver_data=old_host_data,
            taker_data=new_host_data,
        )

        new_host_data = add_events(
            giver_data=old_host_data,
            taker_data=new_host_data,
        )

        assert OLD_HOST_DATA_PLACEHOLDER in new_file_content
        assert NEW_HOST_DATA_PLACEHOLDER in new_file_content

        new_file_content = new_file_content.replace(
            OLD_HOST_DATA_PLACEHOLDER, new_host_data
        )
        new_file_content = new_file_content.replace(
            NEW_HOST_DATA_PLACEHOLDER, old_host_data
        )

        assert OLD_HOST_DATA_PLACEHOLDER not in new_file_content
        assert NEW_HOST_DATA_PLACEHOLDER not in new_file_content

        assert get_name(old_host_data) in new_file_content
        assert get_name(new_host_data) in new_file_content

        response = HttpResponse(new_file_content, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response
    else:
        return HttpResponse(status=405)
