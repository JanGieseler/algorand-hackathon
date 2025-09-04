import { useWallet, Wallet, WalletId } from "@txnlab/use-wallet-react";
import Account from "./Account";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";

interface ConnectWalletInterface {
  openModal: boolean;
  closeModal: () => void;
}

const ConnectWallet = ({ openModal, closeModal }: ConnectWalletInterface) => {
  const { wallets, activeAddress } = useWallet();

  const isKmd = (wallet: Wallet) => wallet.id === WalletId.KMD;
  console.log(wallets);
  console.log(activeAddress);

  return (
    <Dialog open={openModal} onOpenChange={(isOpen) => !isOpen && closeModal()}>
      <DialogContent className="bg-slate-200">
        <DialogHeader>
          <DialogTitle>Select wallet provider</DialogTitle>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          {activeAddress && (
            <>
              <Account />
              <hr className="my-2" />
            </>
          )}

          {!activeAddress &&
            wallets?.map((wallet) => (
              <Button
                data-test-id={`${wallet.id}-connect`}
                variant="outline"
                key={`provider-${wallet.id}`}
                onClick={() => {
                  return wallet.connect();
                }}
                className="flex h-auto items-center justify-start gap-4"
              >
                {!isKmd(wallet) && <img alt={`wallet_icon_${wallet.id}`} src={wallet.metadata.icon} className="w-8 h-8 object-contain" />}
                <span className="truncate">{isKmd(wallet) ? "LocalNet Wallet" : wallet.metadata.name}</span>
              </Button>
            ))}
        </div>

        <DialogFooter>
          <Button variant="secondary" data-test-id="close-wallet-modal" onClick={closeModal}>
            Close
          </Button>
          {activeAddress && (
            <Button
              variant="destructive"
              data-test-id="logout"
              onClick={async () => {
                if (wallets) {
                  const activeWallet = wallets.find((w) => w.isActive);
                  if (activeWallet) {
                    await activeWallet.disconnect();
                  } else {
                    // Required for logout/cleanup of inactive providers
                    // For instance, when you login to localnet wallet and switch network
                    // to testnet/mainnet or vice verse.
                    localStorage.removeItem("@txnlab/use-wallet:v3");
                    window.location.reload();
                  }
                }
              }}
            >
              Logout
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
export default ConnectWallet;
