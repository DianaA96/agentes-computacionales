using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class CarData
{
    public int uniqueID;
    public Vector3 position;
}

public class agentData
{
    public List<Vector3> positions;
}

public class ControlTrafico : MonoBehaviour
{
    // private string url = "https://boids.us-south.cf.appdomain.cloud/";
    private string getAgentsUrl = "http://localhost:8585/getAgents", 
            getObstaclesUrl = "http://localhost:8585/getObstacles", 
            sendConfigUrl = "http://localhost:8585/init", 
            updateUrl = "http://localhost:8585/update", 
            updateLightsUrl= "http://localhost:8585/updateLights";
    private agentData carsData, obstacleData;
    public GameObject carPrefab, obstaclePrefab, floor, semaforo1, semaforo2, semaforo3, semaforo4;
    public int NAgents, width, height;
    GameObject[] agents;
    public float timeToUpdate = 5.0f, timer, dt;
    public float greenlightDuration = 5.0f, redlightDuration = 5.0f;
    List<Vector3> newPositions;
    int status = 2;

    [UnityEngine.Serialization.FormerlySerializedAs("MR_Main")]
    public MeshRenderer lights1, lights2, lights3,lights4;

    void Start()
    {
        carsData = new agentData();
        obstacleData = new agentData();
        newPositions = new List<Vector3>();

        agents = new GameObject[NAgents];

        floor.transform.localScale = new Vector3((float)width / 10, 1, (float)height / 10);
        timer = timeToUpdate;

        for (int i = 0; i < NAgents; i++)
        {
            agents[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
            agents[i].transform.Rotate(new Vector3(0, 90, 0));
        }
           

        StartCoroutine(sendConfiguration());
    }

    private void Update()
    {   
        if(status==2) greenlightDuration -= Time.deltaTime;
        else if(status==1) redlightDuration -= Time.deltaTime;

        float t = timer / timeToUpdate;
        dt = t * t * (3f - 2f * t);

        if (timer >= timeToUpdate)
        {
            timer = 0;
            StartCoroutine(updateSimulation());
        }

        if (newPositions.Count > 1)
        {
            for (int s = 0; s < agents.Length; s++)
            {
                Vector3 interpolated = Vector3.Lerp(agents[s].transform.position, newPositions[s], dt);
                agents[s].transform.localPosition = interpolated;

                Vector3 dir = agents[s].transform.position - newPositions[s];

                timer += Time.deltaTime;
            }
        }

        if (greenlightDuration < 0)
        {
            semaforo1.GetComponent<SemaforoLuz>().MRChangeLeftYield(ref lights1, "Red");
            Debug.Log("Cambio a estatus 1");
            StartCoroutine(updateLightStatus(1));
            status = 1;
            greenlightDuration = 30.0f;
        }

        if (redlightDuration < 0)
        {
            semaforo1.GetComponent<SemaforoLuz>().MRChangeLeftYield(ref lights1, "Green");
            Debug.Log("Cambio a estatus 2");
            StartCoroutine(updateLightStatus(2));
            status = 2;
            redlightDuration = 30.0f;
        }
    }

    IEnumerator updateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(updateUrl);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            StartCoroutine(GetCarsData());
        }
    }

    IEnumerator sendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

        UnityWebRequest www = UnityWebRequest.Post(sendConfigUrl, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetObstacleData());
        }
    }

    IEnumerator updateLightStatus(int lightStatus)
    {
        WWWForm form = new WWWForm();

        form.AddField("semaforos", lightStatus.ToString());
        

        UnityWebRequest www = UnityWebRequest.Post(updateLightsUrl, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log("No se puede actualizar el estatus" + lightStatus +" del semaforo: " + www.error);
        }
        else
        {
            Debug.Log("Estatus de semaforos actualizado!");
        }
    }

    IEnumerator GetCarsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(getAgentsUrl);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            carsData = JsonUtility.FromJson<agentData>(www.downloadHandler.text);

            newPositions.Clear();

            foreach (Vector3 v in carsData.positions)
                newPositions.Add(v);
        }
    }
    IEnumerator GetObstacleData()
    {
        UnityWebRequest www = UnityWebRequest.Get(getObstaclesUrl);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            obstacleData = JsonUtility.FromJson<agentData>(www.downloadHandler.text);

            Debug.Log(obstacleData.positions);

            foreach (Vector3 position in obstacleData.positions)
            {
                Instantiate(obstaclePrefab, position, Quaternion.identity);
            }
        }
    }
}
