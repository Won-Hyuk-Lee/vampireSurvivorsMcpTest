using UnityEngine;

public class WeaponAura : MonoBehaviour
{
    public float dps = 5f;

    void OnTriggerStay2D(Collider2D other)
    {
        // Simple DPS check
        if (other.CompareTag("Monster"))
        {
            var health = other.GetComponent<EnemyHealth>();
            if (health != null)
            {
                health.TakeDamage(dps * Time.deltaTime);
            }
        }
    }
}
