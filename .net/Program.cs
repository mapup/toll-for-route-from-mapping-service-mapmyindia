using System;
using System.IO;
using System.Net;
using RestSharp;

namespace mapmyIndia
{
    public class Program
    {
        public static void Main()
        {
            // Create a request for the URL.
            string api_key="";
            string source_longitude="80.131123";
            string source_latitude="28.552413";
            string destination_longitude="77.113091";
            string destination_latitude="28.544649";
            string url="https://apis.mapmyindia.com/advancedmaps/v1/"+api_key+"/route_adv/driving/"+source_longitude+","+source_latitude+";"+destination_longitude+","+destination_latitude+"?steps=false&rtype=1";
            Console.WriteLine(url);
            WebRequest request = WebRequest.Create(url);
            WebResponse response = request.GetResponse();
            String polyline;
            using (Stream dataStream = response.GetResponseStream())
            {
                // Open the stream using a StreamReader for easy access.
                StreamReader reader = new StreamReader(dataStream);
                // Read the content.
                string responseFromServer = reader.ReadToEnd();
                // Display the content.
                string[] output = responseFromServer.Split(":\"");
                string[] temp = output[3].Split("\"");
                polyline=temp[0];
            }
            // Close the response.
            response.Close();

    /***********Toll Guru API*****************/
            var client = new RestClient("https://dev.tollguru.com/v1/calc/route");
            var request1 = new RestRequest(Method.POST);
            request1.AddHeader("content-type", "application/json");
            request1.AddHeader("x-api-key", "");
            request1.AddParameter("application/json", "{\"source\":\"mapmyindia\" , \"polyline\":\""+polyline+"\" }", ParameterType.RequestBody);
            IRestResponse response1 = client.Execute(request1);        
            var content = response1.Content;
            string[] result = content.Split("tag\":");
            string[] temp1 = result[1].Split(",");
            string cost = temp1[0];
            Console.WriteLine(cost);
        }
    }
}
