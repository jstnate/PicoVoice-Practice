import { SpeechlyClient } from '@speechly/browser-client';

const square = document.getElementById("square");

// Remplacez cette valeur par l'ID de votre application Speechly
const appId = 'your-speechly-app-id';

const speechlyClient = new SpeechlyClient({ appId });

speechlyClient.onSegmentChange((segment) => {
  if (segment.intent.intent === 'move') {
    const directionEntity = segment.entities.find((entity) => entity.type === 'direction');

    if (directionEntity) {
      const direction = directionEntity.value;

      // Mettre à jour la position du carré en fonction de la commande vocale
      if (direction === 'right' || direction === 'droite') {
        square.style.left = (parseFloat(square.style.left) + 10) + 'px';
      } else if (direction === 'left' || direction === 'gauche') {
        square.style.left = (parseFloat(square.style.left) - 10) + 'px';
      } else if (direction === 'top' || direction === 'haut') {
        square.style.top = (parseFloat(square.style.top) - 10) + 'px';
      } else if (direction === 'bottom' || direction === 'bas') {
        square.style.top = (parseFloat(square.style.top) + 10) + 'px';
      }
    }
  }
});

speechlyClient.onError((error) => {
  console.error('Erreur de reconnaissance vocale Speechly:', error);
});

speechlyClient.startContext().catch((error) => {
  console.error('Erreur lors de la connexion à Speechly:', error);
});