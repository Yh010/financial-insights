import React from 'react';

// The official URL for the "Add to Google Wallet" button asset
//const GOOGLE_WALLET_BUTTON_URL = 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/en-us_add_to_google_wallet_add-to-wallet-button.png';

const GOOGLE_WALLET_BUTTON_URL = 'src/assets/add-to-wallet.svg';

interface AgentMessageProps {
  content: string;
}

export function AgentMessage({ content }: AgentMessageProps) {
  // Use a regular expression to find a Google Wallet save link in the text
  const walletUrlMatch = content.match(/(https?:\/\/pay\.google\.com\/gp\/v\/save\/[^\s]+)/);
  const walletUrl = walletUrlMatch ? walletUrlMatch[0] : null;
  console.log(content);
  console.log(walletUrlMatch);
  return (
    <div className="flex items-start gap-3">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-700 text-white font-bold">
        R
      </div>
      <div className="max-w-md rounded-lg rounded-tl-none bg-gray-200 p-3 text-gray-800">
        {walletUrl ? (
          // If a wallet URL is found, display the button
          <div>
            <p className="mb-3">I've created your pass! You can add it to your wallet now.</p>
            <a href={walletUrl} target="_blank" rel="noopener noreferrer">
              <img 
                src={GOOGLE_WALLET_BUTTON_URL} 
                alt="Add to Google Wallet" 
                className="w-48"
              />
            </a>
          </div>
        ) : (
          // Otherwise, just display the plain text
          <p className="whitespace-pre-wrap">{content}</p>
        )}
      </div>
    </div>
  );
}