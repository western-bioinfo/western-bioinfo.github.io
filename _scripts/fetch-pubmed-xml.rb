require 'rest-client'
require 'nokogiri'

# Replace with the name of the author you want to search for
AUTHOR_NAME = 'Shooshtari P[Author]'

# Construct the first query to get the list of PubMed IDs for all papers by the author
url1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=#{AUTHOR_NAME}"
response1 = RestClient.get(url1)
root1 = Nokogiri::XML(response1.body)
id_list = root1.xpath('//IdList/Id').map(&:text).join(',')

# Construct the second query to get the XML data for all papers in the list
url2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=#{id_list}&retmode=xml"
response2 = RestClient.get(url2)

# Print the XML data
file = File.new("assets/pubmed_result.xml", "w")
file.puts(response2.body)
puts response2.body
