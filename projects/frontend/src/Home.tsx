// src/components/Home.tsx
import { useWallet } from "@txnlab/use-wallet-react";
import React, { useState, useEffect } from "react";
import { useSnackbar } from "notistack";
import ConnectWallet from "./components/ConnectWallet";
import Transact from "./components/Transact";
import UploadContent from "./components/UploadContent";
import VerifyContent from "./components/VerifyContent";
import PreviewContent from "./components/PreviewContent";

interface Asset {
  asset_id: {
    value: string;
  };
  description: string;
}

interface AssetsListResponse {
  success: boolean;
  assets: Asset[];
  message: string;
}

interface HomeProps {}

const Home: React.FC<HomeProps> = () => {
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false);
  const [openDemoModal, setOpenDemoModal] = useState<boolean>(false);
  const [openUploadModal, setOpenUploadModal] = useState<boolean>(false);
  const [openVerifyModal, setOpenVerifyModal] = useState<boolean>(false);
  const [openPreviewModal, setOpenPreviewModal] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [verifiedAssets, setVerifiedAssets] = useState<Asset[]>([]);
  const [loadingVerifiedAssets, setLoadingVerifiedAssets] = useState<boolean>(true);
  const [errorVerifiedAssets, setErrorVerifiedAssets] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [transactionId, setTransactionId] = useState<string | null>("");
  const { activeAddress } = useWallet();
  const { enqueueSnackbar } = useSnackbar();

  const toggleWalletModal = () => {
    setOpenWalletModal(!openWalletModal);
  };

  const toggleDemoModal = () => {
    setOpenDemoModal(!openDemoModal);
  };

  const toggleUploadModal = () => {
    setOpenUploadModal(!openUploadModal);
  };

  const toggleVerifyModal = () => {
    setOpenVerifyModal(!openVerifyModal);
  };

  const togglePreviewModal = () => {
    setOpenPreviewModal(!openPreviewModal);
  };

  // Fetch assets from backend
  const fetchAssets = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch("http://localhost:8000/assets");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AssetsListResponse = await response.json();

      if (data.success) {
        setAssets(data.assets);
      } else {
        throw new Error(data.message);
      }
    } catch (e) {
      console.error("Failed to fetch assets:", e);
      setError(e instanceof Error ? e.message : "Failed to fetch assets");
      enqueueSnackbar("Failed to load assets", { variant: "error" });
    } finally {
      setLoading(false);
    }
  };

  const fetchVerifiedAssets = async () => {
    try {
      setLoadingVerifiedAssets(true);
      setErrorVerifiedAssets(null);
      const response = await fetch("http://localhost:8000/verified-assets");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: AssetsListResponse = await response.json();
      if (data.success) {
        setVerifiedAssets(data.assets);
      } else {
        throw new Error(data.message);
      }
    } catch (e) {
      console.error("Failed to fetch verified assets:", e);
      setErrorVerifiedAssets(e instanceof Error ? e.message : "Failed to fetch verified assets");
    } finally {
      setLoadingVerifiedAssets(false);
    }
  };

  // Fetch assets on component mount
  useEffect(() => {
    fetchAssets();
  }, []);

  // Refresh assets when upload modal closes (in case new asset was added)
  useEffect(() => {
    if (!openUploadModal) {
      fetchAssets();
    }
  }, [openUploadModal]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-400 to-teal-600">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-800">AlgoKit Content Platform</h1>
            </div>

            <div className="flex items-center gap-3">
              <button
                data-test-id="verify-content"
                className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 shadow-md hover:shadow-lg active:scale-95"
                onClick={toggleVerifyModal}
              >
                ✅ Verify Content
              </button>

              <button
                data-test-id="upload-content"
                className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 shadow-md hover:shadow-lg active:scale-95"
                onClick={toggleUploadModal}
              >
                📄 Upload Content
              </button>

              <button
                data-test-id="connect-wallet"
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium transition-all duration-200"
                onClick={toggleWalletModal}
              >
                {activeAddress ? "👛 Wallet Connected" : "🔗 Connect Wallet"}
              </button>

              {activeAddress && (
                <button
                  data-test-id="transactions-demo"
                  className="bg-blue-100 hover:bg-blue-200 text-blue-700 px-4 py-2 rounded-lg font-medium transition-all duration-200"
                  onClick={toggleDemoModal}
                >
                  💸 Send ALGO
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">My Content Assets</h2>
          <p className="text-teal-100">Browse and manage uploaded content</p>
        </div>

        {/* Assets Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-white border-t-transparent"></div>
            <span className="ml-4 text-white font-medium">Loading assets...</span>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-300 rounded-lg p-6 text-center">
            <p className="text-red-700 font-medium">Error loading assets: {error}</p>
            <button
              onClick={fetchAssets}
              className="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-all duration-200"
            >
              Retry
            </button>
          </div>
        ) : assets.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <div className="text-6xl mb-4">📄</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No assets yet</h3>
            <p className="text-gray-500 mb-6">Upload your first content asset to get started</p>
            <button
              onClick={toggleUploadModal}
              className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200"
            >
              📄 Upload First Asset
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {assets.map((asset) => (
              <div
                key={asset.asset_id.value}
                className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-6 border border-gray-100 hover:border-teal-200"
              >
                <div className="flex items-start gap-3 mb-4">
                  <div className="text-2xl">📄</div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800 text-lg mb-2 line-clamp-2">{asset.description}</h3>
                    <p className="text-sm text-gray-500 font-mono">ID: {asset.asset_id.value.substring(0, 8)}...</p>
                  </div>
                </div>

                <button
                  className="w-full bg-teal-50 hover:bg-teal-100 text-teal-700 py-2 px-4 rounded-lg font-medium transition-all duration-200 border border-teal-200"
                  onClick={() => {
                    setSelectedAsset(asset);
                    togglePreviewModal();
                  }}
                >
                  🔍 View Details
                </button>
              </div>
            ))}
          </div>
        )}

        {/* My Verified Assets */}
      </main>

      {/* Modals */}
      <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />
      <Transact openModal={openDemoModal} setModalState={setOpenDemoModal} />
      <UploadContent openModal={openUploadModal} setModalState={setOpenUploadModal} setTransactionId={setTransactionId} />
      <VerifyContent openModal={openVerifyModal} setModalState={setOpenVerifyModal} />
      {selectedAsset && <PreviewContent openModal={openPreviewModal} setModalState={setOpenPreviewModal} asset={selectedAsset} />}
    </div>
  );
};

export default Home;
