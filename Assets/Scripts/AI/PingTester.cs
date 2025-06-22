using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class PingTester : MonoBehaviour
{
    private void Start()
    {
        StartCoroutine(PingServer());
    }

    IEnumerator PingServer()
    {
        string url = ApiConfig.GetFullUrl(ApiConfig.Endpoints.Ping);
        UnityWebRequest request = UnityWebRequest.Get(url);
        request.timeout = 15; // Set a timeout for the request

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
            Debug.Log("Ping successful: " + request.downloadHandler.text);
        else
            Debug.LogError("Ping failed: " + request.error);
    }
}