using UnityEngine;

public class EnemyHealth : MonoBehaviour
{
    public float hp = 10f;
    public GameObject gemPrefab;

    void Start()
    {
        if (gemPrefab == null) gemPrefab = Resources.Load<GameObject>("ExpGem");
    }

    public void TakeDamage(float amount)
    {
        hp -= amount;
        if (hp <= 0) Die();
    }

    void Die()
    {
        if (gemPrefab != null)
        {
            Instantiate(gemPrefab, transform.position, Quaternion.identity);
        }
        Destroy(gameObject);
    }
}
