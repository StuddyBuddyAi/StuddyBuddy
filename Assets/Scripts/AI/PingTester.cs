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
        string url = "http://localhost:8000/ping";
        UnityWebRequest request = UnityWebRequest.Get(url);

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
            Debug.Log("Ping successful: " + request.downloadHandler.text);
        else
            Debug.LogError("Ping failed: " + request.error);
    }
}