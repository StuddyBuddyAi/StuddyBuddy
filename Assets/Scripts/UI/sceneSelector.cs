using UnityEngine;
using UnityEngine.SceneManagement;

public class sceneSelectButton : MonoBehaviour
{
    public string sceneName;
    // Start is called before the first frame update


    public void changeScene()
    {
        SceneManager.LoadScene(sceneName);
    }

}
