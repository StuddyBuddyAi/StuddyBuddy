using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class AIClient : MonoBehaviour
{
    public IEnumerator GetSchedule(string jsonPayload)
    {
        UnityWebRequest request = new UnityWebRequest("https://studybuddy-api-w8g5.onrender.com/generate_ai_schedule", "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonPayload);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
            Debug.Log("Response: " + request.downloadHandler.text);
        else
            Debug.LogError("Error: " + request.error);
    }
}
