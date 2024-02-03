$(document).ready(function () {
    var searchPerformed = false;

    $(".sortable").click(function (e) {
        if (!$(e.target).is("input")) {
            if (searchPerformed) {
                searchPerformed = false;
                return;
            }

            var column = $(this).data("column");
            var order = $(this).data("order");

            var newOrder = order === 'asc' ? 'desc' : 'asc';
            $(this).data("order", newOrder);

            $.ajax({
                url: "/sort",
                method: "POST",
                data: { column: column, order: newOrder }, 
                success: function (response) {
                    $("#requisites-table").empty();

                    $.each(response.requisites, function (index, r) {
                        var row = '<tr><td>' + r.id + '</td><td>' + r.payment_type + '</td><td>' + r.account_type + '</td><td>' + r.owner_name + '</td><td>' + r.phone_number + '</td><td>' + r.limit + '</td><td>' + r.account + '</td></tr>';
                        $("#requisites-table").append(row);
                    });

                    $(".sort-indicator").html(''); 
                    var indicator = newOrder === 'asc' ? '&#x2191;' : '&#x2193;';
                    $(".sortable[data-column='" + column + "'] .sort-indicator").html(indicator);
                }
            });
        }
    });

    $(".column-search").on("input", function () {
        searchPerformed = true; 
        var column = $(this).data("column");
        var searchTerm = $(this).val();

        $.ajax({
            url: "/search",
            method: "POST",
            data: { column: column, searchTerm: searchTerm },
            success: function (response) {
                $("#requisites-table").empty();

                $.each(response.requisites, function (index, r) {
                    var row = '<tr><td>' + r.id + '</td><td>' + r.payment_type + '</td><td>' + r.account_type + '</td><td>' + r.owner_name + '</td><td>' + r.phone_number + '</td><td>' + r.limit + '</td><td>' + r.account + '</td></tr>';
                    $("#requisites-table").append(row);
                });
            }
        });
    });
});
