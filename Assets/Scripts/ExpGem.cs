using UnityEngine;

public class ExpGem : MonoBehaviour
{
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.name == "Player" || other.CompareTag("Player"))
        {
            Debug.Log("EXP GEM COLLECTED!");
            Destroy(gameObject);
        }
    }
}
