using UnityEngine;
using System.Collections;

public class EnemySpawner : MonoBehaviour
{
    public GameObject monsterPrefab;
    public float spawnInterval = 3f;
    public float spawnRadius = 10f;

    void Start()
    {
        if (monsterPrefab == null)
        {
            // Fallback load from Resources if not assigned
            monsterPrefab = Resources.Load<GameObject>("Monster");
        }
        StartCoroutine(SpawnRoutine());
    }

    IEnumerator SpawnRoutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(spawnInterval);
            SpawnMonster();
        }
    }

    void SpawnMonster()
    {
        if (monsterPrefab == null) return;

        Vector2 randomPos = Random.insideUnitCircle.normalized * spawnRadius;
        // Assume spawner is at (0,0) or add to spawner's pos
        Vector3 spawnPos = transform.position + (Vector3)randomPos;
        
        Instantiate(monsterPrefab, spawnPos, Quaternion.identity);
    }
}
