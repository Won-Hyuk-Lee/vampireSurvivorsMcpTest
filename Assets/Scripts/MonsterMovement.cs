using UnityEngine;

public class MonsterMovement : MonoBehaviour
{
    public float speed = 2f;
    private Transform player;
    private Rigidbody2D rb;

    void Start()
    {
        // Modern Unity finding (Unity 2023+ prefers FindFirstObjectByType)
        // Check API compatibility, use classic FindObjectOfType for now for safety or try/catch
        player = GameObject.Find("Player")?.transform;
        rb = GetComponent<Rigidbody2D>();
    }

    void FixedUpdate()
    {
        if (player != null && rb != null)
        {
            Vector2 direction = (player.position - transform.position).normalized;
            rb.linearVelocity = direction * speed;
        }
        else if (player == null)
        {
             // Try to find player again if lost (e.g. player died and respawned, or scene reload)
             var p = GameObject.Find("Player");
             if (p) player = p.transform;
             rb.linearVelocity = Vector2.zero;
        }
    }
}
