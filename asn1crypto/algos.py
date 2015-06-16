# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from .core import Any, Choice, Integer, ObjectIdentifier, OctetString, Sequence


# Structures and OIDs in this file are pulled from
# https://tools.ietf.org/html/rfc3279, https://tools.ietf.org/html/rfc4055,
# https://tools.ietf.org/html/rfc5758, https://tools.ietf.org/html/rfc7292,
# http://www.emc.com/collateral/white-papers/h11302-pkcs5v2-1-password-based-cryptography-standard-wp.pdf

class AlgorithmIdentifier(Sequence):
    _fields = [
        ('algorithm', ObjectIdentifier),
        ('parameters', Any, {'optional': True}),
    ]


class HmacAlgorithmId(ObjectIdentifier):
    _map = {
        '1.3.14.3.2.10': 'des_mac',
        '1.2.840.113549.2.7': 'sha1',
        '1.2.840.113549.2.8': 'sha224',
        '1.2.840.113549.2.9': 'sha256',
        '1.2.840.113549.2.10': 'sha384',
        '1.2.840.113549.2.11': 'sha512',
        '1.2.840.113549.2.12': 'sha512_224',
        '1.2.840.113549.2.13': 'sha512_256',
    }


class HmacAlgorithm(Sequence):
    _fields = [
        ('algorithm', HmacAlgorithmId),
        ('parameters', Any, {'optional': True}),
    ]


class DigestAlgorithmId(ObjectIdentifier):
    _map = {
        '1.2.840.113549.2.2': 'md2',
        '1.2.840.113549.2.5': 'md5',
        '1.3.14.3.2.26': 'sha1',
        '2.16.840.1.101.3.4.2.4': 'sha224',
        '2.16.840.1.101.3.4.2.1': 'sha256',
        '2.16.840.1.101.3.4.2.2': 'sha384',
        '2.16.840.1.101.3.4.2.3': 'sha512',
        '2.16.840.1.101.3.4.2.5': 'sha512_224',
        '2.16.840.1.101.3.4.2.6': 'sha512_256',
    }


class DigestAlgorithm(Sequence):
    _fields = [
        ('algorithm', DigestAlgorithmId),
        ('parameters', Any, {'optional': True}),
    ]


# This structure is what is signed with a SignedDigestAlgorithm
class DigestInfo(Sequence):
    _fields = [
        ('digest_algorithm', DigestAlgorithm),
        ('digest', OctetString),
    ]


class SignedDigestAlgorithmId(ObjectIdentifier):
    _map = {
        '1.3.14.3.2.3': 'md5_rsa',
        '1.3.14.3.2.29': 'sha1_rsa',
        '1.3.14.7.2.3.1': 'md2_rsa',
        '1.2.840.113549.1.1.2': 'md2_rsa',
        '1.2.840.113549.1.1.4': 'md5_rsa',
        '1.2.840.113549.1.1.5': 'sha1_rsa',
        '1.2.840.113549.1.1.14': 'sha224_rsa',
        '1.2.840.113549.1.1.11': 'sha256_rsa',
        '1.2.840.113549.1.1.12': 'sha384_rsa',
        '1.2.840.113549.1.1.13': 'sha512_rsa',
        '1.2.840.10040.4.3': 'sha1_dsa',
        '1.3.14.3.2.13': 'sha1_dsa',
        '1.3.14.3.2.27': 'sha1_dsa',
        '2.16.840.1.101.3.4.3.1': 'sha224_dsa',
        '2.16.840.1.101.3.4.3.2': 'sha256_dsa',
        '1.2.840.10045.4.1': 'sha1_ecdsa',
        '1.2.840.10045.4.3.1': 'sha224_ecdsa',
        '1.2.840.10045.4.3.2': 'sha256_ecdsa',
        '1.2.840.10045.4.3.3': 'sha384_ecdsa',
        '1.2.840.10045.4.3.4': 'sha512_ecdsa',
        # For when the digest is specified elsewhere in a Sequence
        '1.2.840.113549.1.1.1': 'rsa',
        '1.2.840.10040.4.1': 'dsa',
        '1.2.840.10045.4': 'ecdsa',
    }


class SignedDigestAlgorithm(Sequence):
    _fields = [
        ('algorithm', SignedDigestAlgorithmId),
        ('parameters', Any, {'optional': True}),
    ]


class Pbkdf2Salt(Choice):
    _alternatives = [
        ('specified', OctetString),
        ('other_source', AlgorithmIdentifier),
    ]


class Pbkdf2Params(Sequence):
    _fields = [
        ('salt', Pbkdf2Salt),
        ('iteration_count', Integer),
        ('key_length', Integer, {'optional': True}),
        ('prf', HmacAlgorithm, {'default': {'algorithm': 'sha1'}}),
    ]


class KdfAlgorithmId(ObjectIdentifier):
    _map = {
        '1.2.840.113549.1.5.12': 'pbkdf2'
    }


class KdfAlgorithm(Sequence):
    _fields = [
        ('algorithm', KdfAlgorithmId),
        ('parameters', Any, {'optional': True}),
    ]
    _oid_pair = ('algorithm', 'parameters')
    _oid_specs = {
        'pbkdf2': Pbkdf2Params
    }


class Rc2Params(Sequence):
    _fields = [
        ('rc2_parameter_version', Integer, {'optional': True}),
        ('iv', OctetString),
    ]


class Rc5ParamVersion(Integer):
    _map = {
        16: 'v1-0'
    }


class Rc5Params(Sequence):
    _fields = [
        ('version', Rc5ParamVersion),
        ('rounds', Integer),
        ('block_size_in_bits', Integer),
        ('iv', OctetString, {'optional': True}),
    ]


class Pbes1Params(Sequence):
    _fields = [
        ('salt', OctetString),
        ('iterations', Integer),
    ]


class EncryptionAlgorithmId(ObjectIdentifier):
    _map = {
        '1.3.14.3.2.7': 'des',
        '1.2.840.113549.3.7': 'tripledes_3key',
        '1.2.840.113549.3.2': 'rc2',
        '1.2.840.113549.3.9': 'rc5',
        '2.16.840.1.101.3.4.1.2': 'aes128',
        '2.16.840.1.101.3.4.1.22': 'aes192',
        '2.16.840.1.101.3.4.1.42': 'aes256',
        # From PKCS#5
        '1.2.840.113549.1.5.13': 'pbes2',
        '1.2.840.113549.1.5.1': 'pbes1_md2_des',
        '1.2.840.113549.1.5.3': 'pbes1_md5_des',
        '1.2.840.113549.1.5.4': 'pbes1_md2_rc2',
        '1.2.840.113549.1.5.6': 'pbes1_md5_rc2',
        '1.2.840.113549.1.5.10': 'pbes1_sha1_des',
        '1.2.840.113549.1.5.11': 'pbes1_sha1_rc2',
        # From PKCS#12
        '1.2.840.113549.1.12.1.1': 'pkcs12_sha1_rc4_128',
        '1.2.840.113549.1.12.1.2': 'pkcs12_sha1_rc4_40',
        '1.2.840.113549.1.12.1.3': 'pkcs12_sha1_tripledes_3key',
        '1.2.840.113549.1.12.1.4': 'pkcs12_sha1_tripledes_2key',
        '1.2.840.113549.1.12.1.5': 'pkcs12_sha1_rc2_128',
        '1.2.840.113549.1.12.1.6': 'pkcs12_sha1_rc2_40',
    }


class EncryptionAlgorithm(Sequence):
    _fields = [
        ('algorithm', EncryptionAlgorithmId),
        ('parameters', Any, {'optional': True}),
    ]

    _oid_pair = ('algorithm', 'parameters')
    _oid_specs = {
        'des': OctetString,
        'tripledes_3key': OctetString,
        'rc2': Rc2Params,
        'rc5': Rc5Params,
        'aes128': OctetString,
        'aes192': OctetString,
        'aes256': OctetString,
        # From PKCS#5
        'pbes1_md2_des': Pbes1Params,
        'pbes1_md5_des': Pbes1Params,
        'pbes1_md2_rc2': Pbes1Params,
        'pbes1_md5_rc2': Pbes1Params,
        'pbes1_sha1_des': Pbes1Params,
        'pbes1_sha1_rc2': Pbes1Params,
        # From PKCS#12
        'pkcs12_sha1_rc4_128': Pbes1Params,
        'pkcs12_sha1_rc4_40': Pbes1Params,
        'pkcs12_sha1_tripledes_3key': Pbes1Params,
        'pkcs12_sha1_tripledes_2key': Pbes1Params,
        'pkcs12_sha1_rc2_128': Pbes1Params,
        'pkcs12_sha1_rc2_40': Pbes1Params,
    }

    @property
    def kdf(self):
        """
        Returns the name of the key derivation function to use.

        :return:
            A unicode from of one of the following: "pbkdf1", "pbkdf2", "pkcs12_kdf"
        """

        encryption_algo = self['algorithm'].native

        if encryption_algo == 'pbes2':
            return self['parameters']['key_derivation_func']['algorithm'].native

        if encryption_algo.find('.') == -1:
            if encryption_algo.find('_') != -1:
                encryption_algo, _ = encryption_algo.split('_', 1)

                if encryption_algo == 'pbes1':
                    return 'pbkdf1'

                if encryption_algo == 'pkcs12':
                    return 'pkcs12_kdf'

            raise ValueError('Encryption algorithm "%s" does not have a registered key derivation function' % encryption_algo)

        raise ValueError('Unrecognized encryption algorithm "%s", can not determine key derivation function' % encryption_algo)

    @property
    def kdf_hmac(self):
        """
        Returns the HMAC algorithm to use with the KDF.

        :return:
            A unicode string of one of the following: "md2", "md5", "sha1", "sha224", "sha256", "sha384", "sha512"
        """

        encryption_algo = self['algorithm'].native

        if encryption_algo == 'pbes2':
            return self['parameters']['key_derivation_func']['parameters']['prf']['algorithm'].native

        if encryption_algo.find('.') == -1:
            if encryption_algo.find('_') != -1:
                _, hmac_algo, _ = encryption_algo.split('_', 2)
                return hmac_algo

            raise ValueError('Encryption algorithm "%s" does not have a registered key derivation function' % encryption_algo)

        raise ValueError('Unrecognized encryption algorithm "%s", can not determine key derivation hmac algorithm' % encryption_algo)

    @property
    def kdf_salt(self):
        """
        Returns the byte string to use as the salt for the KDF.

        :return:
            A byte string
        """

        encryption_algo = self['algorithm'].native

        if encryption_algo == 'pbes2':
            salt = self['parameters']['key_derivation_func']['parameters']['salt']

            if salt.name == 'other_source':
                raise ValueError('Can not determine key derivation salt - the reversed-for-future-use other source salt choice was specified in the PBKDF2 params structure')

            return salt.native

        if encryption_algo.find('.') == -1:
            if encryption_algo.find('_') != -1:
                return self['parameters']['salt'].native

            raise ValueError('Encryption algorithm "%s" does not have a registered key derivation function' % encryption_algo)

        raise ValueError('Unrecognized encryption algorithm "%s", can not determine key derivation salt' % encryption_algo)

    @property
    def kdf_iterations(self):
        """
        Returns the number of iterations that should be run via the KDF.

        :return:
            An integer
        """

        encryption_algo = self['algorithm'].native

        if encryption_algo == 'pbes2':
            return self['parameters']['key_derivation_func']['parameters']['iteration_count'].native

        if encryption_algo.find('.') == -1:
            if encryption_algo.find('_') != -1:
                return self['parameters']['iterations'].native

            raise ValueError('Encryption algorithm "%s" does not have a registered key derivation function' % encryption_algo)

        raise ValueError('Unrecognized encryption algorithm "%s", can not determine key derivation iterations' % encryption_algo)

    @property
    def key_length(self):
        """
        Returns the key length to pass to the cipher/kdf. The PKCS#5 spec does
        not specify a way to store the RC5 key length, however this tends not
        to be a problem since OpenSSL does not support RC5 in PKCS#8 and OS X
        does not provide an RC5 cipher for use in the Security Transforms
        library.

        :raises:
            ValueError - when the key length can not be determined

        :return:
            An integer representing the length in bytes
        """

        encryption_algo = self['algorithm'].native

        cipher_lengths = {
            'des': 8,
            'tripledes_3key': 24,
            'aes128': 16,
            'aes192': 24,
            'aes256': 32,
        }

        if encryption_algo in cipher_lengths:
            return cipher_lengths[encryption_algo]

        if encryption_algo == 'rc2':
            rc2_params = self['parameters'].parsed['encryption_scheme']['parameters'].parsed
            rc2_parameter_version = rc2_params['rc2_parameter_version'].native

            # See page 24 of http://www.emc.com/collateral/white-papers/h11302-pkcs5v2-1-password-based-cryptography-standard-wp.pdf
            encoded_key_bits_map = {
                160: 5,   # 40-bit
                120: 8,   # 64-bit
                58:  16,  # 128-bit
            }

            if rc2_parameter_version in encoded_key_bits_map:
                return encoded_key_bits_map[rc2_parameter_version]

            if rc2_parameter_version >= 256:
                return rc2_parameter_version

            if rc2_parameter_version is None:
                return 4  # 32-bit default

            raise ValueError('Invalid RC2 parameter version found in EncryptionAlgorithm parameters')

        if encryption_algo == 'pbes2':
            key_length = self['parameters']['key_derivation_func']['parameters']['key_length'].native
            if key_length is not None:
                return key_length

            # If the KDF params don't specify the key size, we can infer it from
            # the encryption scheme for all schemes except for RC5. However, in
            # practical terms, neither OpenSSL or OS X support RC5 for PKCS#8
            # so it is unlikely to be an issue that is run into.

            return self['parameters']['encryption_scheme'].key_length

        if encryption_algo.find('.') == -1:
            return {
                'pbes1_md2_des': 8,
                'pbes1_md5_des': 8,
                'pbes1_md2_rc2': 8,
                'pbes1_md5_rc2': 8,
                'pbes1_sha1_des': 8,
                'pbes1_sha1_rc2': 8,
                'pkcs12_sha1_rc4_128': 16,
                'pkcs12_sha1_rc4_40': 5,
                'pkcs12_sha1_tripledes_3key': 24,
                'pkcs12_sha1_tripledes_2key': 16,
                'pkcs12_sha1_rc2_128': 16,
                'pkcs12_sha1_rc2_40': 5,
            }[encryption_algo]

        raise ValueError('Unrecognized encryption algorithm "%s"' % encryption_algo)

    @property
    def encryption_cipher(self):
        """
        Returns the name of the symmetric encryption cipher to use. The key
        length can be retrieved via the .key_length property to disabiguate
        between different variations of TripleDES, AES, and the RC* ciphers.

        :return:
            A unicode string from one of the following: "rc2", "rc5", "des", "tripledes", "aes"
        """

        encryption_algo = self['algorithm'].native

        cipher_map = {
            'des': 'des',
            'tripledes_3key': 'tripledes',
            'aes128': 'aes',
            'aes192': 'aes',
            'aes256': 'aes',
            'rc2': 'rc2',
            'rc5': 'rc5',
        }
        if encryption_algo in cipher_map:
            return cipher_map[encryption_algo]

        if encryption_algo == 'pbes2':
            return self['parameters']['encryption_scheme'].encryption_cipher

        if encryption_algo.find('.') == -1:
            return {
                'pbes1_md2_des': 'des',
                'pbes1_md5_des': 'des',
                'pbes1_md2_rc2': 'rc2',
                'pbes1_md5_rc2': 'rc2',
                'pbes1_sha1_des': 'des',
                'pbes1_sha1_rc2': 'rc2',
                'pkcs12_sha1_rc4_128': 'rc4',
                'pkcs12_sha1_rc4_40': 'rc4',
                'pkcs12_sha1_tripledes_3key': 'tripledes',
                'pkcs12_sha1_tripledes_2key': 'tripledes',
                'pkcs12_sha1_rc2_128': 'rc2',
                'pkcs12_sha1_rc2_40': 'rc2',
            }[encryption_algo]

        raise ValueError('Unrecognized encryption algorithm "%s"' % encryption_algo)

    @property
    def encryption_block_size(self):
        """
        Returns the block size of the encryption cipher, in bytes.

        :return:
            An integer that is the block size in bytes
        """

        encryption_algo = self['algorithm'].native

        cipher_map = {
            'des': 8,
            'tripledes_3key': 8,
            'aes128': 16,
            'aes192': 16,
            'aes256': 16,
            'rc2': 8,
        }
        if encryption_algo in cipher_map:
            return cipher_map[encryption_algo]

        if encryption_algo == 'rc5':
            return self['parameters'].parsed['block_size_in_bits'].native / 8

        if encryption_algo == 'pbes2':
            return self['parameters']['encryption_scheme'].encryption_block_size

        if encryption_algo.find('.') == -1:
            return {
                'pbes1_md2_des': 8,
                'pbes1_md5_des': 8,
                'pbes1_md2_rc2': 8,
                'pbes1_md5_rc2': 8,
                'pbes1_sha1_des': 8,
                'pbes1_sha1_rc2': 8,
                'pkcs12_sha1_rc4_128': 0,
                'pkcs12_sha1_rc4_40': 0,
                'pkcs12_sha1_tripledes_3key': 8,
                'pkcs12_sha1_tripledes_2key': 8,
                'pkcs12_sha1_rc2_128': 8,
                'pkcs12_sha1_rc2_40': 8,
            }[encryption_algo]

        raise ValueError('Unrecognized encryption algorithm "%s"' % encryption_algo)

    @property
    def encryption_iv(self):
        """
        Returns the byte string of the initialization vector for the encryption
        scheme. Only the PBES2 stores the IV in the params. For PBES1, the IV
        is derived from the KDF and this property will return None.

        :return:
            A byte string or None
        """

        encryption_algo = self['algorithm'].native

        if encryption_algo in ('rc2', 'rc5'):
            return self['parameters'].parsed['iv'].native

        # For DES/Triple DES and AES the IV is the entirety of the parameters
        if encryption_algo in ('des', 'tripledes_3key', 'aes128', 'aes192', 'aes256'):
            return self['parameters'].native

        if encryption_algo == 'pbes2':
            return self['parameters']['encryption_scheme'].encryption_iv

        # All of the PBES1 algos use their KDF to create the IV. For the pbkdf1,
        # the KDF is told to generate a key that is an extra 8 bytes long, and
        # that is used for the IV. For the PKCS#12 KDF, it is called with an id
        # of 2 to generate the IV. In either case, we can't return the IV
        # without knowing the user's password.
        if encryption_algo.find('.') == -1:
            return None

        raise ValueError('Unrecognized encryption algorithm "%s"' % encryption_algo)


class Pbes2Params(Sequence):
    _fields = [
        ('key_derivation_func', KdfAlgorithm),
        ('encryption_scheme', EncryptionAlgorithm),
    ]


class Pbmac1Params(Sequence):
    _fields = [
        ('key_derivation_func', KdfAlgorithm),
        ('message_auth_scheme', HmacAlgorithm),
    ]


class Pkcs5MacId(ObjectIdentifier):
    _map = {
        '1.2.840.113549.1.5.14': 'pbmac1',
    }


class Pkcs5MacAlgorithm(Sequence):
    _fields = [
        ('algorithm', Pkcs5MacId),
        ('parameters', Any),
    ]

    _oid_pair = ('algorithm', 'parameters')
    _oid_specs = {
        'pbmac1': Pbmac1Params,
    }


EncryptionAlgorithm._oid_specs['pbes2'] = Pbes2Params  #pylint: disable=W0212
