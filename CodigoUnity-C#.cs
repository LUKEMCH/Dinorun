using UnityEngine;
using UnityEngine.UI;

public class PlayerController : MonoBehaviour
{
    public float speed = 0f; // Velocidade em unidades por segundo (m/s)
    private float acceleration = 2f; // Aceleração inicial em unidades por segundo ao quadrado (m/s²)
    private float doubledAcceleration = 4f; // Aceleração dobrada em unidades por segundo ao quadrado (m/s²)
    private float startDistance;
    private float startTime;
    private float totalDistance; // Distância total percorrida durante o movimento
    private float totalTime; // Tempo total decorrido durante o movimento
    private int clickCount = 0; // Contador de cliques
    private bool isMoving = false;

    public Text speedText;
    public Text accelerationText;
    public Text distanceText;
    public Text timeText;
    public Text averageSpeedText; // Texto para exibir a velocidade média

    private Rigidbody2D rb;
    private Animator animator;

    private float screenWidthInWorldUnits;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        animator = GetComponent<Animator>(); // Pega o componente Animator
        startDistance = transform.position.x;
        startTime = Time.time;

        // Verifique se todos os textos foram encontrados
        if (speedText == null) Debug.LogError("SpeedText não encontrado!");
        if (accelerationText == null) Debug.LogError("AccelerationText não encontrado!");
        if (distanceText == null) Debug.LogError("DistanceText não encontrado!");
        if (timeText == null) Debug.LogError("TimeText não encontrado!");
        if (averageSpeedText == null) Debug.LogError("AverageSpeedText não encontrado!");

        // Calcula a largura da tela em unidades do mundo
        screenWidthInWorldUnits = Camera.main.orthographicSize * Camera.main.aspect * 2;

        UpdateUI();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            clickCount++;

            if (clickCount == 1)
            {
                // Primeiro clique: Aceleração padrão
                acceleration = 2f;
                StartMovement();
            }
            else if (clickCount == 2)
            {
                // Segundo clique: Aceleração dobrada
                acceleration = doubledAcceleration;
                StartMovement();
            }
            else if (clickCount == 3)
            {
                // Terceiro clique: Parar
                StopMovement();
            }
        }

        if (isMoving)
        {
            speed += acceleration * Time.deltaTime;
            rb.velocity = new Vector2(speed, 0);

            // Atualiza a distância total e o tempo total
            totalDistance += speed * Time.deltaTime;
            totalTime = Time.time - startTime;

            // Verifica se o player saiu da tela e o reposiciona
            if (transform.position.x >= screenWidthInWorldUnits / 2)
            {
                transform.position = new Vector2(-screenWidthInWorldUnits / 2, transform.position.y);
            }

            UpdateUI();
        }

        // Atualiza a animação
        animator.SetFloat("Speed", Mathf.Abs(speed));
    }

    void StartMovement()
    {
        isMoving = true;

        // Inicia o movimento apenas na primeira vez (primeiro clique) ou após parar (terceiro clique)
        if (clickCount == 1 || clickCount == 3)
        {
            startDistance = transform.position.x;
            startTime = Time.time;
            totalDistance = 0f; // Reseta a distância total ao iniciar o movimento
        }
    }

    void StopMovement()
    {
        isMoving = false;
        rb.velocity = Vector2.zero;

        // Atualiza a UI com os valores finais
        UpdateUI();

        // Reseta o contador de cliques
        clickCount = 0;

        // Zera os dados após atualizar a UI
        speed = 0f;
    }

    void UpdateUI()
    {
        if (speedText != null) speedText.text = "Velocidade: " + speed.ToString("F2") + " m/s";
        if (accelerationText != null) accelerationText.text = "Aceleração: " + acceleration.ToString("F2") + " m/s²";
        if (distanceText != null) distanceText.text = "Distância: " + totalDistance.ToString("F2") + " m";
        if (timeText != null) timeText.text = "Tempo: " + totalTime.ToString("F2") + " s";

        // Calcula e exibe a velocidade média
        if (averageSpeedText != null)
        {
            if (totalTime > 0)
            {
                float averageSpeed = totalDistance / totalTime;
                averageSpeedText.text = "Velocidade Média: " + averageSpeed.ToString("F2") + " m/s";
            }
            else
            {
                averageSpeedText.text = "Velocidade Média: 0.00 m/s";
            }
        }
    }
}
