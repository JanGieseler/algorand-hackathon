import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { useEffect, useState } from "react";

interface AssetIdResponse {
  asset_id: string;
  description: string;
}

interface Asset {
  asset_id: string;
  description: string;
  content: string;
  location: {
    latitude: number;
    longitude: number;
  };
  timestamp: string;
  creator: string;
  publisher: string;
}

interface PreviewContentProps {
  asset: AssetIdResponse;
  openModal: boolean;
  setModalState: (value: boolean) => void;
}

const PreviewContent: React.FC<PreviewContentProps> = ({ asset, openModal, setModalState }) => {
  const [assetData, setAssetData] = useState<Asset | null>(null);
  useEffect(() => {
    const fetchAsset = async () => {
      const response = await fetch(`http://localhost:8000/assets/${asset.asset_id}`);
      const data = await response.json();
      console.log(data);
      setAssetData(data.asset);
    };
    fetchAsset();
  }, [asset]);

  return (
    <Dialog open={openModal} onOpenChange={setModalState}>
      <DialogContent className="sm:max-w-3xl bg-slate-200">
        <DialogHeader>
          <DialogTitle>Asset Preview</DialogTitle>
          <DialogDescription>Details for asset {assetData?.asset_id}</DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Asset ID</span>
            <span className="col-span-3 break-all">{assetData?.asset_id}</span>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Description</span>
            <span className="col-span-3">{assetData?.description}</span>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Content</span>
            <span className="col-span-3">{assetData?.content}</span>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Location</span>
            <span className="col-span-3">
              {assetData?.location.latitude}, {assetData?.location.longitude}
            </span>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Timestamp</span>
            <span className="col-span-3">{new Date(assetData?.timestamp || "").toLocaleString()}</span>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Creator</span>
            <span className="col-span-3">{assetData?.creator}</span>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <span className="text-right font-bold">Publisher</span>
            <span className="col-span-3">{assetData?.publisher}</span>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PreviewContent;
