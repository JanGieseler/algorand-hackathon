import { useSnackbar } from 'notistack'
import { useState } from 'react'

interface UploadContentInterface {
  openModal: boolean
  setModalState: (value: boolean) => void
}

interface UploadFormData {
  content: string
  publisher: string
  creator: string
  description: string
  timestamp: string
}

const UploadContent = ({ openModal, setModalState }: UploadContentInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  const [formData, setFormData] = useState<UploadFormData>({
    content: '',
    publisher: '',
    creator: '',
    description: '',
    timestamp: ''
  })

  const { enqueueSnackbar } = useSnackbar()

  const handleInputChange = (field: keyof UploadFormData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async () => {
    setLoading(true)

    // Validate required fields
    if (!formData.content.trim() || !formData.publisher.trim() || !formData.creator.trim() || !formData.description.trim()) {
      enqueueSnackbar('Please fill in all fields', { variant: 'warning' })
      setLoading(false)
      return
    }

    try {
      enqueueSnackbar('Uploading content...', { variant: 'info' })
      
      formData.timestamp = new Date(Date.now()).toISOString();
      const response = await fetch('/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        enqueueSnackbar('Content uploaded successfully!', { variant: 'success' })
        // Reset form
        setFormData({
          content: '',
          publisher: '',
          creator: '',
          description: '',
          timestamp: ''
        })
        setModalState(false)
      } else {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
    } catch (e) {
      console.error('Upload failed:', e)
      enqueueSnackbar('Failed to upload content', { variant: 'error' })
    }

    setLoading(false)
  }

  const isFormValid = formData.content.trim() && formData.publisher.trim() && formData.creator.trim() && formData.description.trim()

  return (
    <dialog id="upload_modal" className={`modal ${openModal ? 'modal-open' : ''}`} style={{ display: openModal ? 'block' : 'none' }}>
      <div className="modal-backdrop bg-black bg-opacity-50" onClick={() => setModalState(false)} />
      <div className="modal-box max-w-3xl bg-white shadow-2xl border-0">
        {/* Header */}
        <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
          <h3 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            📄 Upload Content
          </h3>
          <button 
            className="btn btn-sm btn-circle btn-ghost text-gray-500 hover:text-gray-700"
            onClick={() => setModalState(false)}
          >
            ✕
          </button>
        </div>
        
        <div className="space-y-8 px-2">
          {/* Content Text Area */}
          <div className="form-control">
            <label className="label pb-3">
              <span className="label-text text-base font-semibold text-gray-700 flex items-center gap-2">
                📝 Content
              </span>
              <span className="label-text-alt text-gray-500">Required</span>
            </label>
            <textarea
              data-test-id="content-input"
              placeholder="Paste your plain text content here..."
              className="w-full h-40 resize-none p-4 text-sm leading-relaxed border-2 border-gray-200 rounded-xl focus:border-teal-500 focus:ring-4 focus:ring-teal-100 focus:outline-none transition-all duration-300 shadow-sm hover:shadow-md hover:border-gray-300 bg-gray-50 focus:bg-white"
              value={formData.content}
              onChange={(e) => handleInputChange('content', e.target.value)}
            />
            <label className="label pt-2">
              <span className="label-text-alt text-gray-500">{formData.content.length} characters</span>
            </label>
          </div>

          {/* Two Column Layout for Publisher and Creator */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Publisher Input */}
            <div className="form-control">
              <label className="label pb-3">
                <span className="label-text text-base font-semibold text-gray-700 flex items-center gap-2">
                  🏢 Publisher
                </span>
                <span className="label-text-alt text-gray-500">Required</span>
              </label>
              <input
                type="text"
                data-test-id="publisher-input"
                placeholder="Enter publisher name"
                className="w-full p-4 text-sm border-2 border-gray-200 rounded-xl focus:border-teal-500 focus:ring-4 focus:ring-teal-100 focus:outline-none transition-all duration-300 shadow-sm hover:shadow-md hover:border-gray-300 bg-gray-50 focus:bg-white"
                value={formData.publisher}
                onChange={(e) => handleInputChange('publisher', e.target.value)}
              />
            </div>

            {/* Creator Input */}
            <div className="form-control">
              <label className="label pb-3">
                <span className="label-text text-base font-semibold text-gray-700 flex items-center gap-2">
                  👤 Creator
                </span>
                <span className="label-text-alt text-gray-500">Required</span>
              </label>
              <input
                type="text"
                data-test-id="creator-input"
                placeholder="Enter creator name"
                className="w-full p-4 text-sm border-2 border-gray-200 rounded-xl focus:border-teal-500 focus:ring-4 focus:ring-teal-100 focus:outline-none transition-all duration-300 shadow-sm hover:shadow-md hover:border-gray-300 bg-gray-50 focus:bg-white"
                value={formData.creator}
                onChange={(e) => handleInputChange('creator', e.target.value)}
              />
            </div>
          </div>

          {/* Description Input */}
          <div className="form-control">
            <label className="label pb-3">
              <span className="label-text text-base font-semibold text-gray-700 flex items-center gap-2">
                📋 Description
              </span>
              <span className="label-text-alt text-gray-500">Required</span>
            </label>
                          <input
              type="text"
              data-test-id="description-input"
              placeholder="Enter content description"
              className="w-full p-4 text-sm border-2 border-gray-200 rounded-xl focus:border-teal-500 focus:ring-4 focus:ring-teal-100 focus:outline-none transition-all duration-300 shadow-sm hover:shadow-md hover:border-gray-300 bg-gray-50 focus:bg-white"
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="modal-action mt-10 pt-8 border-t border-gray-200">
          <div className="flex gap-4 w-full px-2">
            <button 
              type="button"
              className="flex-1 py-3 px-6 rounded-xl font-semibold text-gray-700 bg-white border-2 border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all duration-300 shadow-sm hover:shadow-md active:scale-95" 
              onClick={() => setModalState(false)}
            >
              Cancel
            </button>
            <button
              type="button"
              data-test-id="submit-upload"
              className={`flex-1 py-3 px-6 rounded-xl font-semibold text-white transition-all duration-300 ${
                !isFormValid || loading 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-teal-600 hover:bg-teal-700 hover:shadow-lg active:scale-95 shadow-md'
              }`}
              onClick={handleSubmit}
              disabled={!isFormValid || loading}
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                  Uploading...
                </div>
              ) : (
                <div className="flex items-center justify-center gap-2">
                  🚀 Upload Content
                </div>
              )}
            </button>
          </div>
        </div>
      </div>
    </dialog>
  )
}

export default UploadContent



