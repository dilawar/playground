require "jekyll-import";
JekyllImport::Importers::WordpressDotCom.run({
  "source" => "./dilawar039sblog.wordpress.2020-06-14.001.xml",
  "no_fetch_images" => false,
  "assets_folder" => "assets/images"
})
