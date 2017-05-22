using System;
using System.Collections.Generic;
using Windows.UI;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Media;
using Windows.Web.Http;
using Windows.Data.Json;
using System.Threading;
using Windows.Storage;

namespace ShanghaiTech
{
    public sealed partial class MainPage : Page
    {
        private HttpClient _httpClient;
        private CancellationTokenSource _cts;
        ApplicationDataContainer localSettings = Windows.Storage.ApplicationData.Current.LocalSettings;
        public MainPage()
        {
            this.InitializeComponent();
            if (localSettings.Values.ContainsKey("usr"))
            {
                usr.Text = localSettings.Values["usr"].ToString();
                psw.Password = localSettings.Values["psw"].ToString();
                rsw.IsOn = true;
            }
        }
        private async void DoVerify(object sender, RoutedEventArgs e)
        {
            Status_tb.Foreground = new SolidColorBrush(Colors.Black);
            Status_tb.Text = "";
            _httpClient = new HttpClient();
            _cts = new CancellationTokenSource();
            var postData = new HttpFormUrlEncodedContent(
                new List<KeyValuePair<string, string>>
                {
                    new KeyValuePair<string, string>("userName", usr.Text),
                    new KeyValuePair<string, string>("password", psw.Password),
                    new KeyValuePair<string,string> ("hasValidateCode","false"),
                    new KeyValuePair<string, string>("authLan","zh_CN"),
                    new KeyValuePair<string,string>("rememberPwd","true")
                }
            );
            postData.Headers.ContentType = new Windows.Web.Http.Headers.HttpMediaTypeHeaderValue("application/x-www-form-urlencoded");
            _httpClient.DefaultRequestHeaders.Add("Cookie", "JSESSIONID = gd0ycxjk6zniolwq9");
            try
            {
                HttpResponseMessage response = await _httpClient.PostAsync(
                    new Uri("https://controller1.net.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!login.action"),
                    postData).AsTask(_cts.Token); // 取消请求的方式改为通过 CancellationTokenSource 来实现了
                var jres = JsonValue.Parse(response.Content.ToString()).GetObject();
                if (jres.GetNamedBoolean("success"))
                {
                    Status_tb.Foreground = new SolidColorBrush(Colors.Blue);
                    Status_tb.Text = "Success";
                }
                else
                {
                    Status_tb.Foreground = new SolidColorBrush(Colors.Red);
                    Status_tb.Text = jres.GetNamedString("message");
                }
            }
            catch (Exception)
            {
                Status_tb.Foreground = new SolidColorBrush(Colors.Red);
                Status_tb.Text = "Verify failed. Please check your Internet connection";
            }
        }
        private void rClick(object sender, RoutedEventArgs e)
        {
            if (rsw.IsOn)
            {
                localSettings.Values["usr"] = usr.Text;
                localSettings.Values["psw"] = psw.Password;
            }
            else
            {
                localSettings.Values.Remove("usr");
                localSettings.Values.Remove("psw");
            }
        }
    }
}
