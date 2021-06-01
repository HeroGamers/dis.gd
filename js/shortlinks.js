// Wait for the DOM to load
$(document).ready(function() {
    // Get URL pararameters - using them to remove elements from the JSON file
    const urlParams = new URLSearchParams(window.location.search)
    const shortlink_type = urlParams.get("type")
    // console.log(shortlink_type)

    // Get json file
    $.getJSON("shortlinks.json", function(json) {
        // console.log(json)
        $.each(json, function(i) {
            // Skip if it doesn't match criteria in URL parameter
            if (shortlink_type && json[i].type) {
                let type;
                switch (shortlink_type.toLowerCase()) {
                    case "articles":
                    case "article":
                        type = "article"
                        break
                    case "blogposts":
                    case "blogpost":
                        type = "blogpost"
                        break
                    case "external website":
                    case "external websites":
                    case "external":
                    case "externalwebsite":
                    case "externalwebsites":
                        type = "external website"
                        break
                    case "website":
                    case "websites":
                        type = "website"
                        break
                    case "form":
                    case "forms":
                        type = "form"
                        break
                    case "store":
                    case "stores":
                        type = "store"
                        break
                    case "server invite":
                    case "server":
                    case "servers":
                    case "serverinvite":
                    case "serverinvites":
                        type = "server invite"
                        break
                }
                if (type) {
                    // If type doesn't match, skip
                    if (json[i].type.toLowerCase() !== type) {
                        return
                    }
                }
            }

            let linkText = json[i].link.toString()
            if (json[i].links) {
                linkText = json[i].links.join("<br/>")
            }

            // Add the link element to the body of the table
            $("#shortLinkTable tbody").append(
                "<tr>" +
                "    <th scope='row' class='shortLinkLink'>" +
                "        <a href='https://dis.gd/"+json[i].link+"' target='_blank'>" + linkText + "</a>" +
                "    </th>" +
                "    <td class='shortLinkType'>"+json[i].type+"</td>" +
                "    <td class='shortLinkDescription'>" + json[i].description + "</td>" +
                "    <td class='shortLinkRedirect'>" +
                "        <a href="+json[i].redirect+" target='_blank'>" + json[i].redirect + "</a>" +
                "    </td>" +
                "    <td class='shortLinkUsefulness'>" + json[i].usefulness + "</td>" +
                "</tr>"
            )
        })
        // Now that we've put the data in, we can initialize the Bootstrap Table
        $("#shortLinkTable").bootstrapTable()
    })
})
