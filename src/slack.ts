import {App} from '@slack/bolt';

if (
  ['SLACK_TOKEN', 'SLACK_SIGNING_SECRET', 'SLACK_CHANNEL'].filter(
    (x) => process.env[x],
  ).length !== 3
)
  throw new Error('Slack credentials missing in env');
const app = new App({
  token: process.env.SLACK_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
});

export const notifyOnSlack = ({id, name, error}: {id; name; error?}) => {
  console.log('posting to slack');
  return app.client.chat.postMessage({
    channel: process.env.SLACK_CHANNEL!,
    text: error
      ? `
        <https://mentorsearcher.netlify.app/search#${id}|${name}> search has failed. Please try a different search or contact an administrator.
      `
      : `
        <https://mentorsearcher.netlify.app/search#${id}|${name}> search has been *completed*. Please click the link to download the results. 
      `,
  });
};
