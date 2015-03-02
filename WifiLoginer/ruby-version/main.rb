require 'net/http'
require 'securerandom'
# require 'net/https'

basePath = "https://controller.shanghaitech.edu.cn:8445/PortalServer"
loginAction = "/Webauth/webAuthAction!login.action"

def encodeURIComponent(string)
  return URI.escape(string, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"))
end

lang = "zh_CN"
uri = URI.parse(basePath + loginAction)
username, password = ARGV[0], ARGV[1]
cookie = SecureRandom.hex.upcase
params = {
  "userName" => encodeURIComponent(username),
  "password" => encodeURIComponent(password),
  "hasValidateCode" => false,
  "authLan" => encodeURIComponent(lang)
}

https_connection = Net::HTTP.new(uri.host, uri.port)
https_connection.use_ssl = true
request = Net::HTTP::Post.new(uri.path)
request.set_form_data(params)
request["Content-Type"] = "application/x-www-form-urlencoded"
request["Cookie"] = "JSESSIONID=" + cookie
response = https_connection.request(request)

response_hash = eval(response.body.gsub(/:/, "=>").gsub(/null/, "nil"))
response_hash_data = response_hash["data"]

if response_hash["success"] == true
  puts "**Login Succeed!**"
  puts "Account:    " + response_hash_data["account"]
  puts "IP Address: " + response_hash_data["ip"]
  puts "Type:       " + response_hash_data["loginType"].to_s
else
  puts "**Login Failed**"
  puts response_hash["message"]
end