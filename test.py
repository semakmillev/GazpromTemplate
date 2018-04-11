from PIL import Image, ImageCms, JpegImagePlugin, PngImagePlugin
# from subprocess import call
import piexif

# call("exiftool.exe -XResolution=100 -YResolution=100 1.jpg")

im = Image.open("1.png")
p = ImageCms.getOpenProfile("ISOcoated_v2_300_eci.icc")
t = ImageCms.buildTransformFromOpenProfiles(ImageCms.get_display_profile(), "ISOcoated_v2_300_eci.icc", "RGBA", "CMYK")
im = ImageCms.applyTransform(im, t)
im.save("1.pdf", "PDF", resolution=200.0)
'''
im = Image.open("300.jpg")
r = piexif.load("out.jpg")
zeroth_ifd = {piexif.ImageIFD.Make: u"Canon",
              piexif.ImageIFD.XResolution: (3000000, 10000),
              piexif.ImageIFD.YResolution: (3000000, 10000),
              piexif.ImageIFD.Software: u"piexif"
              }
exif_ifd = {piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
            piexif.ExifIFD.LensMake: u"LensMake",
            piexif.ExifIFD.Sharpness: 65535,
            piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
            }
gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSAltitudeRef: 1,
           piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
           }
first_ifd = {piexif.ImageIFD.Make: u"Canon",
             piexif.ImageIFD.XResolution: (40, 1),
             piexif.ImageIFD.YResolution: (40, 1),
             piexif.ImageIFD.Software: u"piexif"
             }

exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd}
exif_bytes = piexif.dump(exif_dict)
im.save("out.jpg", exif=exif_bytes)
#et = exiftool.ExifTool("exiftool.exe")

im = Image.open("1.png", dpi = (100,100))
im.info["dpi"] = (50.1, 50.1)
im.save("1.png", dpi=(40.,40.1))
# final.save("res.png", dpi=80.1)
p = ImageCms.getOpenProfile("ISOcoated_v2_300_eci.icc")
t = ImageCms.buildTransformFromOpenProfiles(ImageCms.get_display_profile(), "ISOcoated_v2_300_eci.icc", "RGBA", "CMYK")
im = ImageCms.applyTransform(im, t)
im.save("1.jpg", dpi=(40.,40.1))
'''
# im.save('res.png', dpi=(600.0,600.0))
# im = im.convert('CMYK')
# im = Image.open('300.jpg')
# i = 1
# im.save("300_1.jpg", dpi=(500, 500))
'''

dp = ImageCms.get_display_profile()
pRGBA = ImageCms.createProfile("LAB")


im = ImageCms.applyTransform(im, t)
im.save("0.jpg", "JPEG")
'''
# im.save("2.jpg", icc_profile=p.profile)

# f = open("tmp.icc","a")
# f.write(icc)
# f.close()
