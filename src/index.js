const Scanner = require('./core/scanner');
const Organizer = require('./core/organizer');
const PrivacyGuard = require('./core/privacy-guard');
const VirtualViews = require('./core/virtual-views');
const ForgeManager = require('./platforms/forge-manager');
const FreeAIService = require('./ai/free-ai-service');
const ShowcaseGenerator = require('./viral/showcase-generator');
const { startServer } = require('./server/app');

module.exports = {
  Scanner,
  Organizer,
  PrivacyGuard,
  VirtualViews,
  ForgeManager,
  FreeAIService,
  ShowcaseGenerator,
  startServer
};
