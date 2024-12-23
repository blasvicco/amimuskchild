import Abstract from './abstract';

class Facecheck extends Abstract {
  /**
   * Constructor
  **/
  constructor() {
    super();
    this.resource = 'facecheck';
    this._updateEndpoint();
    this.constants.UPLOAD = `${this.constants.ENDPOINT}/predict/`;
  }

  get(id) {
    throw new Exception('Not supported.');
  }

  list(id) {
    throw new Exception('Not supported.');
  }

  save(obj) {
    throw new Exception('Not supported.');
  }

  interpret(response) {
    const feeling = {
      0: 'sorry',
      1: 'glad',
      2: 'happy',
      3: 'extremely happy',
      4: 'enormously proud and extremely happy',
    }[response.score];

    const negation = {
      0: 'too happy',
      1: 'disappointed',
      2: 'sad',
      3: 'too upset',
      4: 'extremely sad',
    }[response.score];

    return {
      'MUSK': `We are ${feeling} to say that the most advanced AI technology has detected, with ${response.confidence} confidence, that YOU ARE the result of Elon Müsk's in-vitro fertilization experiment using his genes.`,
      'TRUMP': `The cutting-edge most advanced AI tech has analyzed your face and concluded... you might be just a bit too old to join the Elon Müsk biological dynasty. But don't get ${negation} too quickly—the AI has identified, with ${response.confidence} confidence, that you are most likely biologically related to Donald Trümp.`,
    }[response.prediction];
  }
}

export default new Facecheck();
