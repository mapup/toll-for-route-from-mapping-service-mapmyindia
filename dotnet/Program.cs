using System;
using System.IO;
using System.Net;
using RestSharp;
namespace mapmyIndia
{
    static class Constants
    {
        public const string MAPMYINDIA_API_KEY = Environment.GetEnvironmentVariable("MAPMYINDIA_API_KEY");
        public const string MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1";

        public const string TOLLGURU_API_KEY = Environment.GetEnvironmentVariable("TOLLGURU_API_KEY");
        public const string TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
        public const string POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

        // New Delhi
        public const string source_latitude = "28.68932119156764";
        public const string source_longitude = "77.18609677688849";
        // Mumbai
        public const string destination_latitude = "19.092580173664984";
        public const string destination_longitude = "72.89902799500808";
    }

    public class Program
    {
        public static string get_Response(string source_latitude, string source_longitude, string destination_latitude, string destination_longitude)
        {
            string api_key = Constants.MAPMYINDIA_API_KEY;
            string url = Constants.MAPMYINDIA_API_URL + "/" + api_key + "/route_adv/driving/" + source_longitude + "," + source_latitude + ";" + destination_longitude + "," + destination_latitude + "?geometries=polyline&overview=full";
            WebRequest request = WebRequest.Create(url);
            WebResponse response = request.GetResponse();
            String polyline;
            using (Stream dataStream = response.GetResponseStream())
            {
                StreamReader reader = new StreamReader(dataStream);
                string responseFromServer = reader.ReadToEnd();
                Console.WriteLine(responseFromServer);
                string[] output = responseFromServer.Split("\"geometry\":\"");
                string[] temp = output[1].Split("\"");
                polyline = temp[0];
            }
            response.Close();
            return (polyline);
        }
        public static string Post_Tollguru(string polyline)
        {
            var client = new RestClient(Constants.TOLLGURU_API_URL + "/" + Constants.POLYLINE_ENDPOINT);
            var request1 = new RestRequest(Method.POST);
            request1.AddHeader("content-type", "application/json");
            request1.AddHeader("x-api-key", "");
            request1.AddParameter("application/json", "{\"source\":\"mapmyindia\" , \"polyline\":\"" + polyline + "\" }", ParameterType.RequestBody);
            IRestResponse response1 = client.Execute(request1);
            var content = response1.Content;
            //Console.WriteLine(content);
            string[] result = content.Split("tag\":");
            string[] temp1 = result[1].Split(",");
            string cost = temp1[0];
            return cost;
        }
        public static void Main()
        {
            string polyline = get_Response(Constants.source_latitude, Constants.source_longitude, Constants.destination_latitude, Constants.destination_longitude);
            Console.WriteLine(Post_Tollguru(polyline));
        }
    }
}
