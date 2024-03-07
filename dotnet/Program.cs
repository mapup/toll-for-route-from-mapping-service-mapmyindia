using System;
using System.IO;
using System.Net;
using RestSharp;
using System.Collections.Generic;
using System.Text.Json;

namespace mapmyIndia
{
    using obj = Dictionary<string, object>;
    public class Program
    {

        private static string MAPMYINDIA_API_KEY = Environment.GetEnvironmentVariable("MAPMYINDIA_API_KEY");
        private static string MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1";

        private static string TOLLGURU_API_KEY = Environment.GetEnvironmentVariable("TOLLGURU_API_KEY");
        private static string TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
        private static string POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

        // New Delhi
        private static string source_latitude = "28.68932119156764";
        private static string source_longitude = "77.18609677688849";
        // Mumbai
        private static string destination_latitude = "19.092580173664984";
        private static string destination_longitude = "72.89902799500808";

        private static obj request_params = new obj {
          { "vehicle", new obj {
              { "type", "2AxlesAuto" },
          }},
          { "departure_time", "2021-01-05T09:46:08Z" },
        };

        public static string get_Response(string source_latitude, string source_longitude, string destination_latitude, string destination_longitude)
        {
            string api_key = MAPMYINDIA_API_KEY;
            string url = MAPMYINDIA_API_URL + "/" + api_key + "/route_adv/driving/" + source_longitude + "," + source_latitude + ";" + destination_longitude + "," + destination_latitude + "?geometries=polyline&overview=full";
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
            var client = new RestClient(TOLLGURU_API_URL + "/" + POLYLINE_ENDPOINT);
            var request1 = new RestRequest(Method.POST);
            request1.AddHeader("content-type", "application/json");
            request1.AddHeader("x-api-key", TOLLGURU_API_KEY);
            request_params.AddRange(new obj {
                { "source", "mapmyindia" },
                { "polyline", polyline },
            });
            request1.AddParameter("application/json", JsonSerializer.Serialize(request_params), ParameterType.RequestBody);
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
            string polyline = get_Response(source_latitude, source_longitude, destination_latitude, destination_longitude);
            Console.WriteLine(Post_Tollguru(polyline));
        }
    }
}

// Extension method to add range to a dictionary
public static class DictionaryExtensions
{
    public static void AddRange<TKey, TValue>(this Dictionary<TKey, TValue> dictionary, IDictionary<TKey, TValue> range)
    {
        if (dictionary == null)
        {
            throw new ArgumentNullException(nameof(dictionary));
        }

        if (range == null)
        {
            throw new ArgumentNullException(nameof(range));
        }

        foreach (var kvp in range)
        {
            dictionary[kvp.Key] = kvp.Value;
        }
    }
}
