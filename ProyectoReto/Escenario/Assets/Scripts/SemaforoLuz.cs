using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SemaforoLuz : MonoBehaviour
{
    //Enums for controller:
    public enum iLightControllerEnum { Regular, LeftTurn, MasterLeft1, MasterLeft2, Red }
    //Enums for actual lights:
    public enum iLightStatusEnum { Regular, LeftTurn, MasterLeft, Red, RightTurn }
    public enum iLightSubStatusEnum { Green, Yellow, Red }
    public enum iLightYieldSubStatusEnum { Green, Yellow, Red, YellowTurn, GreenTurn }

   
    [UnityEngine.Serialization.FormerlySerializedAs("LightsObj")]
    public GameObject[] lightsObjects;

   
    [UnityEngine.Serialization.FormerlySerializedAs("MR_Main")]
    public MeshRenderer mainMR;

    [UnityEngine.Serialization.FormerlySerializedAs("iLightStatus")]
    public iLightStatusEnum lightStatus = iLightStatusEnum.Red;
    [UnityEngine.Serialization.FormerlySerializedAs("iLightSubStatus")]
    public iLightYieldSubStatusEnum lightSubStatus = iLightYieldSubStatusEnum.Green;

    [UnityEngine.Serialization.FormerlySerializedAs("bLeft")]
    private bool isLeft = false;
    [UnityEngine.Serialization.FormerlySerializedAs("bRight")]
    private bool isRight = false;
    [UnityEngine.Serialization.FormerlySerializedAs("bMain")]
    private bool isMain = false;
    [UnityEngine.Serialization.FormerlySerializedAs("bUseSharedMaterial")]
    private bool isUsingSharedMaterial = false;
    [UnityEngine.Serialization.FormerlySerializedAs("bLeftTurnYieldOnGreen")]
    private bool isLeftTurnYieldOnGreen = true;
    [UnityEngine.Serialization.FormerlySerializedAs("bLightsEnabled")]
    private bool isLightsEnabled = true;

    void Start()
    {
        MRChangeLeftYield(ref mainMR, "Green");
    }


    public void MRChangeLeftYield(ref MeshRenderer _MR, string _lightYieldSub)
    {
        Material meshMaterial;

        if (isUsingSharedMaterial)
        {
            meshMaterial = _MR.sharedMaterial;
        }
        else
        {
            meshMaterial = _MR.material;
        }


        if (_lightYieldSub == "Green")
        {
            meshMaterial.mainTextureOffset = isUsingSharedMaterial ? new Vector2(0.667f, 0f) : new Vector2(0.4f, 0f);
        }
        else if (_lightYieldSub == "Yellow")
        {
            meshMaterial.mainTextureOffset = isUsingSharedMaterial ? new Vector2(0.334f, 0f) : new Vector2(0.2f, 0f);
        }
        else if (_lightYieldSub == "Red")
        {
            meshMaterial.mainTextureOffset = new Vector2(0f, 0f);
        }
        else if (_lightYieldSub == "YellowTurn")
        {
            meshMaterial.mainTextureOffset = new Vector2(0.6f, 0f);
        }
        else if (_lightYieldSub == "GreenTurn")
        {
            meshMaterial.mainTextureOffset = new Vector2(0.8f, 0f);
        }
    }


    // Update is called once per frame
    void Update()
    {
        
    }
}
