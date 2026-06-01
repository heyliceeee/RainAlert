# 🌤 Weather Alert Bot

Um sistema automático de alertas meteorológicos que monitoriza as próximas 12 horas e envia notificações personalizadas através do Telegram. O objetivo é fornecer avisos úteis e imediatos sobre condições relevantes, ajudando a planear o dia com antecedência.

---

## 🔍 O que o sistema faz

- Obtém previsões meteorológicas para as próximas 12 horas com base na localização configurada.  
- Analisa cada período previsto e identifica condições importantes.  
- Gera alertas claros e organizados sempre que ocorre um fenómeno relevante.  
- Envia notificações diretamente para um chat do Telegram.

---

## 🌦 Condições monitorizadas

O sistema deteta automaticamente:

- **🌧 Chuva**  
- **⛈ Trovoada**  
- **🌦 Chuva fraca (drizzle)**  
- **🌨 Neve**  
- **🌫 Nevoeiro**  
- **🔥 Temperaturas elevadas** (acima do limite definido)

Cada condição é apresentada com a hora prevista e, no caso do calor, também com a temperatura estimada.

---

## 📩 Como funcionam os alertas

Sempre que é identificada uma condição relevante:

- É criada uma mensagem estruturada e fácil de ler.  
- A mensagem inclui apenas fenómenos significativos, evitando notificações desnecessárias.  
- O alerta é enviado automaticamente para o utilizador através do Telegram, utilizando formatação Markdown para maior clareza.

Se não houver nada importante a reportar, o sistema permanece silencioso.