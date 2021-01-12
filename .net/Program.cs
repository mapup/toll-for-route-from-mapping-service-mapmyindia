using System;
using System.IO;
using System.Net;

namespace mapmyIndia
{
    public class Program
    {
        public static void Main()
        {
            // Create a request for the URL.
            string api_key="zsrz71km9hpjwzf5x3ussubuecoce3gq";
            string source_longitude="80.131123";
            string source_latitude="28.552413";
            string destination_longitude="77.113091";
            string destination_latitude="28.544649";
            string url="https://apis.mapmyindia.com/advancedmaps/v1/"+api_key+"/route_adv/driving/"+source_longitude+","+source_latitude+";"+destination_longitude+","+destination_latitude+"?steps=false&rtype=1";
            Console.WriteLine(url);
            WebRequest request = WebRequest.Create(url);
            //WebRequest request = WebRequest.Create(
            //  "https://apis.mapmyindia.com/advancedmaps/v1/zsrz71km9hpjwzf5x3ussubuecoce3gq/route_adv/driving/80.131123,28.552413;77.113091,28.544649?steps=false&rtype=1");
            // If required by the server, set the credentials.
            // Get the response.
            WebResponse response = request.GetResponse();
            // Display the status.
            //Console.WriteLine(((HttpWebResponse)response).StatusDescription);
            String polyline;
            // Get the stream containing content returned by the server.
            // The using block ensures the stream is automatically closed.           
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
            Console.WriteLine(polyline);
            

            // Close the response.
            response.Close();
        }
    }
}