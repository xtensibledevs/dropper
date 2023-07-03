
Object = require 'common/classicobject'
Maintainer = require 'common/maintainer'
python = require("python")

dropper_config = python.execute("from dropper_cli import config")

DropImage = Object:extend()

function DropImage:new(properties)
	self.image_id = properties.image_id
	self.image_name = properties.image_name
	self.maintainer = Maintainer.new(properties.maintainer) 
	self.created_at = properties.created_at
	self.modifier_at = properties.modifier_at
	self.py_dropImage = dropper_config.Image()
	self.py_dropImage.set_drop_image(properties)
end

function DropImage:get(secure_download)
	if secure_download == true then
		self.secure_download()
	self.download()
end

function DropImage:download(props)
	self.py_dropImage.download(props)
end

function DropImage:secure_download(props)
	self.py_dropImage.secure_download(props)
end


return DropImage