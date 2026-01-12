import React, { useState, useEffect } from 'react';
import { X, Save, Loader, User, Calendar, Mail, Phone, MapPin, Hash, BookOpen, Layers } from 'lucide-react';
import api from '../api/axios';

const StudentModal = ({ isOpen, onClose, onSubmit, initialData = null, departments }) => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        father_name: '',
        mother_name: '',
        roll_number: '',
        email: '',
        password: '',
        phone_number: '',
        date_of_birth: '',
        address: '',
        department_id: '',
        batch_id: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [localBatches, setLocalBatches] = useState([]);

    // Fetch batches when department changes
    useEffect(() => {
        const fetchBatches = async () => {
            if (!formData.department_id) {
                setLocalBatches([]);
                return;
            }
            try {
                const response = await api.get('/batches/dropdown', {
                    params: { department_id: formData.department_id }
                });
                setLocalBatches(response.data);
            } catch (err) {
                console.error("Error fetching batches:", err);
            }
        };
        fetchBatches();
    }, [formData.department_id]);

    useEffect(() => {
        if (initialData) {
            setFormData({
                first_name: initialData.first_name || '',
                last_name: initialData.last_name || '',
                father_name: initialData.father_name || '',
                mother_name: initialData.mother_name || '',
                roll_number: initialData.roll_number || '',
                email: initialData.email || '',
                password: '',
                phone_number: initialData.phone_number || '',
                date_of_birth: initialData.date_of_birth || '',
                address: initialData.address || '',
                department_id: initialData.department_id || '',
                batch_id: initialData.batch_id || ''
            });
        } else {
            setFormData({
                first_name: '',
                last_name: '',
                father_name: '',
                mother_name: '',
                roll_number: '',
                email: '',
                password: '',
                phone_number: '',
                date_of_birth: '',
                address: '',
                department_id: '',
                batch_id: ''
            });
        }
        setError('');
    }, [initialData, isOpen]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (!formData.first_name || !formData.last_name || !formData.roll_number || !formData.department_id || !formData.batch_id) {
                throw new Error("Please fill in all required fields.");
            }
            if (!initialData && !formData.password) {
                throw new Error("Password is required for new students.");
            }
            await onSubmit(formData);
            onClose();
        } catch (err) {
            setError(err.message || "An error occurred.");
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    const InputField = ({ label, name, type = "text", icon: Icon, required = false, disabled = false }) => (
        <div>
            <label className="block text-xs font-bold text-gray-400 mb-1.5 uppercase tracking-wider">{label} {required && <span className="text-red-500">*</span>}</label>
            <div className="relative group">
                {Icon && <Icon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 group-focus-within:text-accent-purple transition-colors" size={18} />}
                <input
                    type={type}
                    name={name}
                    value={formData[name]}
                    onChange={handleChange}
                    disabled={disabled}
                    className={`w-full ${Icon ? 'pl-10' : 'pl-4'} pr-4 py-2.5 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none text-gray-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-gray-600`}
                    required={required}
                />
            </div>
        </div>
    );

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="bg-dark-900 border border-white/10 rounded-3xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto animate-in zoom-in-95 duration-200 relative">

                {/* Background Glow */}
                <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0 rounded-3xl">
                    <div className="absolute top-[-20%] right-[-20%] w-[300px] h-[300px] bg-accent-purple/10 rounded-full blur-[80px]"></div>
                </div>

                <div className="relative z-10">
                    {/* Header */}
                    <div className="flex justify-between items-center p-6 border-b border-white/10 sticky top-0 bg-dark-900/95 backdrop-blur-md z-10">
                        <div>
                            <h2 className="text-2xl font-bold text-white tracking-tight">
                                {initialData ? 'Edit Student' : 'Add New Student'}
                            </h2>
                            <p className="text-gray-400 text-sm mt-0.5">Enter student details below.</p>
                        </div>
                        <button onClick={onClose} className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-full transition-all">
                            <X size={24} />
                        </button>
                    </div>

                    {/* Body */}
                    <form onSubmit={handleSubmit} className="p-8 space-y-8">
                        {error && (
                            <div className="bg-red-500/10 text-red-400 p-4 rounded-2xl text-sm font-medium border border-red-500/20 flex items-center gap-2">
                                <div className="w-1.5 h-1.5 rounded-full bg-red-500"></div>
                                {error}
                            </div>
                        )}

                        <div className="space-y-6">
                            <h3 className="text-xs font-bold text-accent-purple uppercase tracking-widest border-b border-white/10 pb-2">Personal Information</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <InputField label="First Name" name="first_name" icon={User} required />
                                <InputField label="Last Name" name="last_name" icon={User} required />
                                <InputField label="Father's Name" name="father_name" icon={User} required />
                                <InputField label="Mother's Name" name="mother_name" icon={User} required />
                                <InputField label="Date of Birth" name="date_of_birth" type="date" icon={Calendar} required />
                            </div>
                        </div>

                        <div className="space-y-6">
                            <h3 className="text-xs font-bold text-accent-purple uppercase tracking-widest border-b border-white/10 pb-2">Academic Details</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <InputField label="Roll Number" name="roll_number" icon={Hash} required disabled={!!initialData} />

                                <div>
                                    <label className="block text-xs font-bold text-gray-400 mb-1.5 uppercase tracking-wider">Department <span className="text-red-500">*</span></label>
                                    <div className="relative group">
                                        <Layers className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 group-focus-within:text-accent-purple transition-colors" size={18} />
                                        <select name="department_id" value={formData.department_id} onChange={handleChange} className="w-full pl-10 pr-4 py-2.5 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none text-gray-200 font-medium appearance-none cursor-pointer" required>
                                            <option value="">Select Dept</option>
                                            {departments.map(d => <option key={d.department_id} value={d.department_id}>{d.department_name}</option>)}
                                        </select>
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-xs font-bold text-gray-400 mb-1.5 uppercase tracking-wider">Batch <span className="text-red-500">*</span></label>
                                    <div className="relative group">
                                        <BookOpen className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 group-focus-within:text-accent-purple transition-colors" size={18} />
                                        <select name="batch_id" value={formData.batch_id} onChange={handleChange} className="w-full pl-10 pr-4 py-2.5 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none text-gray-200 font-medium appearance-none cursor-pointer" required>
                                            <option value="">Select Batch</option>
                                            {localBatches.map(b => <option key={b.batch_id} value={b.batch_id}>{b.batch_name}</option>)}
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-6">
                            <h3 className="text-xs font-bold text-accent-purple uppercase tracking-widest border-b border-white/10 pb-2">Contact Information</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <InputField label="Email" name="email" type="email" icon={Mail} required disabled={!!initialData} />
                                <InputField label="Phone Number" name="phone_number" icon={Phone} required />
                                {!initialData && <InputField label="Password" name="password" type="password" icon={Hash} required />}
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-gray-400 mb-1.5 uppercase tracking-wider">Address <span className="text-red-500">*</span></label>
                                <div className="relative group">
                                    <MapPin className="absolute left-3 top-3 text-gray-500 group-focus-within:text-accent-purple transition-colors" size={18} />
                                    <textarea name="address" value={formData.address} onChange={handleChange} className="w-full pl-10 pr-4 py-2.5 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none text-gray-200 font-medium resize-none" rows="3" required></textarea>
                                </div>
                            </div>
                        </div>

                        {/* Footer */}
                        <div className="flex justify-end gap-3 pt-6 border-t border-white/10">
                            <button type="button" onClick={onClose} className="px-6 py-2.5 text-gray-400 font-bold hover:bg-white/10 hover:text-white rounded-xl transition-all active:scale-95">
                                Cancel
                            </button>
                            <button type="submit" disabled={loading} className="px-8 py-2.5 bg-accent-purple text-white font-bold rounded-xl hover:bg-accent-purple/90 transition-all flex items-center gap-2 shadow-[0_0_20px_rgba(139,92,246,0.3)] active:scale-95 disabled:opacity-70 disabled:active:scale-100">
                                {loading ? <Loader size={18} className="animate-spin" /> : <Save size={18} />}
                                {initialData ? 'Update Student' : 'Create Student'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default StudentModal;
