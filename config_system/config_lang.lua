--[[
FROM - From statement defines which image to download and start from.
--]]
function drop.from(image_id, drop_name)
	image = Image({image_id=image_id, secure_download=True})
	dropperpy:pyExtractImageAs(image_id, drop_name)
end

function drop.maintainer(firsname, lastname, contact)
	maintainer = Maintainer({firsname=firsname, lastname=lastname, contact=contact})
	dropperpy:pyApplyMaintainerInfo(maintainer)