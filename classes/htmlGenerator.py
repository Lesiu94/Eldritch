def makeInvestigatorsForChoose(invList):
    htmlString = "<div class=\"row\">"
    invCount = len(invList)

    for i in range(0, invCount):
        if i > 0 and i % 3 == 0:
            htmlString += " </div> " \
                          " <div class=\"row\"> "
        htmlString += " <div class=\"col-md-4\"> <p>  <div class=\"form-check\">" \
                      "<label class=\"form-check-label\">" \
                      "<input class=\"form-check-input\" type=\"checkbox\" name=\"Investigator\" value=\"\">" \
                      + invList[i] + "</label> </div> </p> </div>"
    htmlString += "</div>"
    return htmlString
